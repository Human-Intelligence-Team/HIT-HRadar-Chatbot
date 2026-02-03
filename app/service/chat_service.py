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
                # Hybrid Search (Semantic + Lexical)
                raw_docs = self.vector.search(
                    query=message,
                    company_id=company_id,
                    limit=30
                )
                
                if not raw_docs:
                    return "관련 문서를 찾을 수 없습니다."

                def get_roots(text):
                    # Simple heuristic roots for Korean
                    particles = ["은", "는", "이", "가", "을", "를", "에", "의", "로", "으로", "도", "만", "에서", "부터", "까지"]
                    words = text.split()
                    roots = []
                    for w in words:
                        clean_w = w.strip("?.!,")
                        # Remove suffixes
                        for p in particles:
                            if clean_w.endswith(p) and len(clean_w) > len(p):
                                clean_w = clean_w[:-len(p)]
                                break
                        if len(clean_w) >= 2:
                            roots.append(clean_w)
                    return roots

                def get_bigrams(text):
                    clean = text.replace(" ", "")
                    return {clean[i:i+2] for i in range(len(clean)-1)}

                query_roots = get_roots(message)
                query_bigrams = get_bigrams(message)
                
                scored_results = []
                # Define common 'filler' or 'intent' words that shouldn't trigger mandatory match alone
                fillers = {"무엇", "정의", "설명", "방법", "절차", "어떻게", "언제", "어디서", "누가", "왜", "궁금", "알려줘"}
                salient_roots = [r for r in query_roots if r not in fillers]

                for d in raw_docs:
                    payload = d["payload"]
                    semantic_score = d["score"]
                    doc_title = payload.get("docTitle", "").replace(" ", "")
                    section_title = payload.get("sectionTitle", "").replace(" ", "")
                    content = payload.get("content", "")
                    
                    # Lexical Scoring
                    lexical_score = 0
                    has_salient_match = False
                    
                    for root in query_roots:
                        is_salient = root in salient_roots
                        match_found = False
                        
                        if section_title and root in section_title:
                            lexical_score += 5.0
                            match_found = True
                        elif doc_title and root in doc_title:
                            lexical_score += 3.0
                            match_found = True
                        elif root in content:
                            lexical_score += 0.5
                            match_found = True
                        
                        if is_salient and match_found:
                            has_salient_match = True
                    
                    # 2. Bigram Overlap (Focused on Section Title for precision)
                    target_text = section_title if section_title else doc_title
                    target_bigrams = get_bigrams(target_text)
                    overlap = query_bigrams.intersection(target_bigrams)
                    lexical_score += len(overlap) * 0.5

                    # Mandatory Match implementation:
                    # If we have salient keywords but none match, we penalize heavily
                    if salient_roots and not has_salient_match:
                        final_score = -1.0 # Force below threshold
                    else:
                        final_score = semantic_score + lexical_score
                        
                    scored_results.append((final_score, semantic_score, lexical_score, payload))
                
                scored_results.sort(key=lambda x: x[0], reverse=True)
                
                logger.info(f"--- Sophisticated Hybrid Search Results (Query: '{message}') ---")
                for i, (f_score, s_score, l_score, doc) in enumerate(scored_results[:3]):
                    logger.info(f"Rank {i+1}: Total={f_score:.2f} (Sem={s_score:.2f}, Lex={l_score:.2f}) | Doc='{doc.get('docTitle')}' | Section='{doc.get('sectionTitle')}'")
                
                # Relevance Guard
                if not scored_results or scored_results[0][0] < 0.5:
                    return "죄송합니다. 요청하신 내용은 현재 등록된 회사 제도 및 규정에서 찾을 수 없습니다. 인사업무나 규정에 관련한 질문을 부탁드립니다."

                return scored_results[0][3].get("content", "내용을 찾을 수 없습니다.")
            except QdrantError as e:
                logger.error(f"Error accessing VectorStore for DOCUMENT route: {e}")
                return "문서 검색 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."


        if route == Route.PERSONAL:
            logger.info("Responding to PERSONAL route.")
            return "개인/조직 데이터 기능은 준비 중입니다."

        logger.info("Responding with default SMALL_TALK message.")
        return "안녕하세요. HRadar 챗봇입니다."
