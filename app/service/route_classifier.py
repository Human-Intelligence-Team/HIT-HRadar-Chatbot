from enum import Enum

class Route(Enum):
    DOCUMENT = "DOCUMENT"
    PERSONAL = "PERSONAL"
    SMALL_TALK = "SMALL_TALK"

class RouteClassifier:
    def classify(self, text: str) -> Route:
        t = text.lower()

        if any(k in t for k in ["내 ", "나의", "우리", "팀"]):
            return Route.PERSONAL

        if any(k in t for k in ["기준", "방법", "절차", "규정"]):
            return Route.DOCUMENT

        return Route.SMALL_TALK
