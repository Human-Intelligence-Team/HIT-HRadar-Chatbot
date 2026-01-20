from app.domain.intent import Intent
from app.infra.hr_client import HrClient
from app.infra.vector_store import VectorStore
from app.infra.llm_client import LlmClient


class ChatService:
    def __init__(self):
        self.hr = HrClient()
        self.vector = VectorStore()
        self.llm = LlmClient()

    def handle(self, intent: Intent, message: str, user_id: int) -> str:
        # ===== 개인 데이터 (Spring HR API) =====
        if intent == Intent.MY_EVALUATION:
            data = self.hr.get_my_evaluation(user_id)
            return self.llm.generate(
                f"이번 평가 결과는 {data['grade']} ({data['rank']})입니다."
            )

        if intent == Intent.MY_COMPETENCY:
            data = self.hr.get_my_competency(user_id)
            return self.llm.generate(
                f"현재 역량 점수는 {data['score']}점입니다."
            )

        # ===== 조직 =====
        if intent == Intent.ORG_STRUCTURE:
            return self.hr.get_org_structure()

        # ===== 평가/리포트 =====
        if intent == Intent.REPORT_STATUS:
            data = self.hr.get_report_status()
            return f"현재 평가는 {data['status']}이며 마감일은 {data['deadline']}입니다."

        # ===== 정책/문서 (Vector DB) =====
        if intent in (
                Intent.POLICY_EVALUATION,
                Intent.POLICY_COMPETENCY,
                Intent.POLICY_NOTICE,
        ):
            contexts = self.vector.search(message, top_k=3)  # list[str]
            if not contexts:
                # 문서가 없으면 추측 금지
                return "관련 문서를 찾지 못했어요. 질문을 조금 더 구체적으로 입력해 주세요."

            return self.llm.answer_with_context(
                question=message,
                contexts=contexts,
            )

        # ===== 가이드/네비 =====
        if intent == Intent.GUIDE_EVALUATION:
            return "평가는 [평가관리 > 평가 진행] 메뉴에서 수행합니다."

        if intent == Intent.NAV_REPORT:
            return "/report/main"

        # ===== 기타 =====
        if intent == Intent.SMALL_TALK:
            return "안녕하세요 🙂 HRadar 챗봇입니다."

        return "질문을 이해하지 못했습니다. 조금 더 구체적으로 말씀해 주세요."
