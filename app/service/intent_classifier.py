from app.domain.intent import Intent

class IntentClassifier:
    """
    자연어 → 시스템 의도(Intent)
    - deterministic(규칙 기반) 우선
    - 예측 가능 / 테스트 용이
    """

    def classify(self, message: str) -> Intent:
        msg = message.lower()

        # 개인
        if "내" in msg:
            if "평가" in msg:
                return Intent.MY_EVALUATION
            if "역량" in msg:
                return Intent.MY_COMPETENCY

        # 조직
        if "조직" in msg or "조직도" in msg:
            return Intent.ORG_STRUCTURE

        # 평가/리포트
        if "평가" in msg:
            if "상태" in msg or "진행" in msg:
                return Intent.REPORT_STATUS
            if "결과" in msg:
                return Intent.REPORT_RESULT
            if "어떻게" in msg or "방법" in msg:
                return Intent.GUIDE_EVALUATION

        # 정책/문서
        if "제도" in msg or "정책" in msg:
            if "평가" in msg:
                return Intent.POLICY_EVALUATION
            if "역량" in msg:
                return Intent.POLICY_COMPETENCY

        if "공지" in msg:
            return Intent.POLICY_NOTICE

        # 네비
        if "화면" in msg or "페이지" in msg:
            return Intent.NAV_REPORT

        # 기타
        if "안녕" in msg or "고마워" in msg:
            return Intent.SMALL_TALK

        return Intent.UNKNOWN
