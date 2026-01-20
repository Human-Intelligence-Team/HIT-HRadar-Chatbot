from datetime import datetime
from app.infra.mongo import chat_logs

def append_message(session_id: str, user_id: int, role: str, text: str, intent=None):
    chat_logs.update_one(
        {"sessionId": session_id},
        {
            "$setOnInsert": {
                "sessionId": session_id,
                "userId": user_id,
                "createdAt": datetime.utcnow(),
            },
            "$push": {
                "messages": {
                    "role": role,
                    "text": text,
                    "intent": intent,
                    "timestamp": datetime.utcnow(),
                }
            },
            "$set": {
                "updatedAt": datetime.utcnow(),
            },
        },
        upsert=True,
    )
