from app.infra.vector_store import VectorStore, QdrantError
from app.infra.rule_based_llm_client import RuleBasedLlmClient
from app.service.rule_based_route_classifier import Route
from app.core.settings import settings
import logging

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.vector = VectorStore.get_instance()
        self.llm = RuleBasedLlmClient()

    def handle(self, route: Route, message: str, company_id: int):
        logger.info(f"Handling message: '{message}' for company_id: {company_id} with route: {route}")

        if route == Route.DOCUMENT:
            try:
                # Widen the search net to ensure we catch definitions even if they rank lower semantically
                raw_docs = self.vector.search(
                    query=message,
                    company_id=company_id,
                    limit=20
                )
                logger.info(f"Raw documents from VectorStore (Count: {len(raw_docs)})")

                if not raw_docs:
                    return "관련 문서를 찾을 수 없습니다."

                def normalize_token(token):
                    # Expanded particle list for better root extraction
                    particles = [
                        "은", "는", "이", "가", "을", "를", "에", "의", "로", "으로", 
                        "도", "만", "에게", "께", "한테", "에서", "이란", "란", "인가요", "해요", "돼", "뭐", "야"
                    ]
                    for p in particles:
                        if token.endswith(p) and len(token) > len(p):
                            return token[:-len(p)]
                    return token.strip("?.!,")

                query_clean = message.replace(" ", "")
                query_tokens = message.split()
                query_root_tokens = [normalize_token(t) for t in query_tokens]
                query_root_set = {t for t in query_root_tokens if len(t) >= 2}
                
                query_bigrams = set()
                for token in query_root_tokens:
                    if len(token) >= 2:
                        query_bigrams.update({token[i:i+2] for i in range(len(token)-1)})
                
                # Broad intent detection
                is_definition_query = any(k in message for k in ["정의", "의미", "뜻", "무엇", "란", "설명", "개요", "머야"])
                is_procedure_query = any(k in message for k in ["절차", "방법", "순서", "단계", "어떻게", "프로세스", "신청", "기안", "보고", "사용", "긴급", "언제", "사유"])
                
                def calculate_heuristic_score(p, v_score):
                    content = p.get("content", "")
                    title = p.get("title", "")
                    chunk_id_str = str(p.get("chunkId", "unnamed"))
                    
                    score = 0
                    
                    # Tier 1: Title Core Match (Aggressive)
                    clean_title = title.replace(" ", "")
                    title_bigrams = {clean_title[i:i+2] for i in range(len(clean_title)-1)}
                    
                    if clean_title and (clean_title in query_clean or query_clean in clean_title):
                        score += 300 
                    
                    # Tier 2: Keyword Importance Weighting (Position Sensitive)
                    common_verbs = {"사용", "하다", "있다", "되다", "없다", "받다", "내다"}
                    sentences = [s.strip() for s in content.replace("\n", ". ").split(".") if s.strip()]
                    
                    for q_token in query_root_set:
                        if q_token in content:
                            # Base Boost
                            if q_token in clean_title or q_token in title_bigrams:
                                score += 30 # Context match
                            elif q_token in common_verbs:
                                score += 10 # Common verb
                            else:
                                score += 250 # High boost for specific unique intent terms (e.g. "긴급")

                            # Position Boost: If word is near the beginning of a sentence
                            for sentence in sentences:
                                if sentence.startswith(q_token) or (len(sentence) > len(q_token)+1 and sentence[1:len(q_token)+1] == q_token):
                                    score += 100 # Match at start of sentence (very strong signal)
                                    break 

                    # Tier 3: Directional Intent Boosts
                    if is_definition_query:
                        if any(k in content for k in ["정의", "이란", "은 다음과 같다", "의미한다", "목적", "말한다"]):
                            score += 150
                    
                    if is_procedure_query:
                        if any(k in content for k in ["절차", "방법", "순서", "단계", "프로세스", "신청", "보고", "기안", "위원회", "가능", "서류"]):
                            score += 150
                    
                    # Tier 4: Structural Priority
                    try:
                        if "_chunk_" in chunk_id_str:
                            chunk_idx = int(chunk_id_str.split("_chunk_")[-1])
                        else:
                            chunk_idx = 10
                    except:
                        chunk_idx = 10
                    
                    if is_definition_query and chunk_idx < 1:
                        score += 50
                    if is_procedure_query and chunk_idx >= 1:
                        score += 80 # Prioritize body chunks for procedure/emergency queries

                    # Tier 5: Fine-grained Overlap
                    shared_bigrams = query_bigrams.intersection(title_bigrams)
                    score += len(shared_bigrams) * 50 
                    
                    # Tier 6: Original Semantic Score
                    score += (v_score * 100)
                    
                    return score

                scored_results = []
                for d in raw_docs:
                    payload = d["payload"]
                    v_score = d["score"]
                    final_score = calculate_heuristic_score(payload, v_score)
                    scored_results.append((final_score, payload))
                
                scored_results.sort(key=lambda x: x[0], reverse=True)
                
                logger.info(f"--- Top 3 Heuristic Scores (Query: '{message}') ---")
                for i, (score, doc) in enumerate(scored_results[:3]):
                    logger.info(f"Rank {i+1}: Overall={score:.2f} | Title='{doc.get('title')}' | Content='{doc.get('content')[:30]}...'")
                
                return scored_results[0][1].get("content", "내용을 찾을 수 없습니다.")
            except QdrantError as e:
                logger.error(f"Error accessing VectorStore for DOCUMENT route: {e}")
                return "문서 검색 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."


        if route == Route.PERSONAL:
            logger.info("Responding to PERSONAL route.")
            return "개인/조직 데이터 기능은 준비 중입니다."

        logger.info("Responding with default SMALL_TALK message.")
        return "안녕하세요. HRadar 챗봇입니다."
