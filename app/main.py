from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.core.settings import settings

app = FastAPI(title=settings.APP_NAME)

app.include_router(chat_router)
