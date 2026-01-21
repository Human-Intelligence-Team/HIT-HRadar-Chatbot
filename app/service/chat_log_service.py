from datetime import datetime
from app.infra.mongo import chat_logs

def append_message(session_id, user_id, role, text, route):
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
                    "route": route,
                    "timestamp": datetime.utcnow(),
                }
            },
            "$set": {"updatedAt": datetime.utcnow()},
        },
        upsert=True,
    )
