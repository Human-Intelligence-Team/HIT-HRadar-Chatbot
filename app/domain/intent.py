from enum import Enum

class Intent(Enum):
    # ======================
    # MY (개인 데이터)
    # ======================
    MY_PROFILE = "MY_PROFILE"
    MY_COMPETENCY = "MY_COMPETENCY"
    MY_EVALUATION = "MY_EVALUATION"
    MY_REPORT = "MY_REPORT"

    # ======================
    # ORG (조직 / 구성원)
    # ======================
    ORG_STRUCTURE = "ORG_STRUCTURE"
    ORG_MEMBER = "ORG_MEMBER"
    ORG_ROLE = "ORG_ROLE"

    # ======================
    # REPORT / COMPETENCY
    # ======================
    REPORT_CYCLE = "REPORT_CYCLE"
    REPORT_STATUS = "REPORT_STATUS"
    REPORT_RESULT = "REPORT_RESULT"
    REPORT_COMPARE = "REPORT_COMPARE"

    # ======================
    # POLICY / NOTICE
    # ======================
    POLICY_EVALUATION = "POLICY_EVALUATION"
    POLICY_COMPETENCY = "POLICY_COMPETENCY"
    POLICY_NOTICE = "POLICY_NOTICE"

    # ======================
    # GUIDE / NAV
    # ======================
    GUIDE_EVALUATION = "GUIDE_EVALUATION"
    GUIDE_REPORT = "GUIDE_REPORT"

    NAV_EVALUATION = "NAV_EVALUATION"
    NAV_REPORT = "NAV_REPORT"

    # ======================
    # ETC
    # ======================
    SMALL_TALK = "SMALL_TALK"
    UNKNOWN = "UNKNOWN"
