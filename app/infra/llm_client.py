import google.generativeai as genai
from app.core.settings import settings

class LlmClient:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-3-flash-preview")

    def answer_with_context(self, question: str, context: str) -> str:
        prompt = f"""
너는 HR 시스템 챗봇이다.
아래 문서만 근거로 답변하라.

[문서]
{context}

[질문]
{question}

- 문서에 없는 내용은 추측하지 말 것
- 모르면 "관련 문서를 찾을 수 없습니다"라고 답할 것
"""
        return self.model.generate_content(prompt).text.strip()
