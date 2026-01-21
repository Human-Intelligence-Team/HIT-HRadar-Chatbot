from app.infra.vector_store import VectorStore
from app.infra.llm_client import LlmClient
from app.service.route_classifier import Route

class ChatService:
    def __init__(self):
        self.vector = VectorStore()
        self.llm = LlmClient()

    def handle(self, route: Route, message: str, company_id: int):
        if route == Route.DOCUMENT:
            docs = self.vector.search(
                query=message,
                company_id=company_id,
            )
            if not docs:
                return "관련 문서를 찾을 수 없습니다."

            context = "\n".join(d["content"] for d in docs)
            return self.llm.answer_with_context(message, context)

        if route == Route.PERSONAL:
            return "개인/조직 데이터 기능은 준비 중입니다."

        return "안녕하세요. HRadar 챗봇입니다."
