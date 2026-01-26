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
        if route == Route.DOCUMENT:
            try:
                raw_docs = self.vector.search(
                    query=message,
                    company_id=company_id,
                )
                
                # Filter documents by relevance score
                relevant_docs = [
                    d["payload"] for d in raw_docs if d["score"] >= settings.RELEVANCE_THRESHOLD
                ]

                if not relevant_docs:
                    return "관련 문서를 찾을 수 없습니다."

                context = "\n".join(d["content"] for d in relevant_docs)
                return self.llm.answer_with_context(message, context)
            except QdrantError as e:
                logger.error(f"Error accessing VectorStore for DOCUMENT route: {e}")
                return "문서 검색 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."


        if route == Route.PERSONAL:
            return "개인/조직 데이터 기능은 준비 중입니다."

        return "안녕하세요. HRadar 챗봇입니다."
