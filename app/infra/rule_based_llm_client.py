class RuleBasedLlmClient:
    def __init__(self):
        pass

    def answer_with_context(self, question: str, context: str) -> str:
        # This is a simplified, rule-based approach.
        # In a real scenario, you might have more sophisticated rules or
        # integrate with a lighter-weight model or a template-based response system.

        if not context:
            return "관련 문서를 찾을 수 없습니다."
        
        # For demonstration, we'll just return a combination of the question and context
        # or a generic answer based on the presence of context.
        return f"다음은 문서 기반 답변입니다: {context[:200]}..." # Truncate context for brevity
