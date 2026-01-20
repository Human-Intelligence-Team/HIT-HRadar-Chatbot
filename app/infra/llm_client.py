from openai import OpenAI
from app.core.settings import settings

class LlmClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def generate(self, text: str) -> str:
        return text  # 단순 응답용 (MY_* 등)

    def answer_with_context(self, question: str, contexts: list[str]) -> str:
        context_text = "\n".join(contexts)

        prompt = f"""
너는 HRadar 사내 HR 챗봇이다.
아래 문서 내용을 근거로 질문에 답변하라.
문서에 없는 내용은 추측하지 마라.

[문서]
{context_text}

[질문]
{question}
"""

        res = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        return res.choices[0].message.content.strip()
