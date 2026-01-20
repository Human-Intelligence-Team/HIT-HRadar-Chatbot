from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app.service.intent_classifier import IntentClassifier
from app.service.chat_service import ChatService
from app.service.chat_log_service import append_message

router = APIRouter(prefix="/chat", tags=["chat"])

classifier = IntentClassifier()
service = ChatService()

class ChatRequest(BaseModel):
    message: str
    sessionId: str

@router.post("")
def chat(
        req: ChatRequest,
        x_user_id: str = Header(None),
        x_user_role: str = Header(None),
        x_company_id: str = Header(None),
):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = int(x_user_id)

    # Intent 분류
    intent = classifier.classify(req.message)

    # user 로그 저장
    append_message(
        session_id=req.sessionId,
        user_id=user_id,
        role="user",
        text=req.message,
        intent=intent.value,
    )

    # 처리 전략 실행
    answer = service.handle(intent, req.message, user_id)

    # bot 로그 저장
    append_message(
        session_id=req.sessionId,
        user_id=user_id,
        role="bot",
        text=answer,
        intent=intent.value,
    )

    return {
        "intent": intent.value,
        "answer": answer,
    }
