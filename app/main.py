from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.index import router as index_router
from app.core.settings import settings

app = FastAPI(title=settings.APP_NAME)

app.include_router(chat_router)
app.include_router(index_router)