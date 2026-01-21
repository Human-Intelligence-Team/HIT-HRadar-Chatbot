from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app.service.route_classifier import RouteClassifier
from app.service.chat_service import ChatService
from app.service.chat_log_service import append_message

router = APIRouter(prefix="/chat")

classifier = RouteClassifier()
service = ChatService()

class ChatRequest(BaseModel):
    message: str
    sessionId: str

@router.post("")
def chat(req: ChatRequest, x_user_id: str = Header(None)):
    if not x_user_id:
        raise HTTPException(status_code=401)

    route = classifier.classify(req.message)

    append_message(req.sessionId, int(x_user_id), "user", req.message, route.value)
    answer = service.handle(route, req.message)
    append_message(req.sessionId, int(x_user_id), "bot", answer, route.value)

    return {"answer": answer}
