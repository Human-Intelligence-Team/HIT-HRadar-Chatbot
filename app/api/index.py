from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import List
from app.service.vector_index_service import VectorIndexService

router = APIRouter(prefix="/index")

service = VectorIndexService()


class ChunkPayload(BaseModel):
    chunkId: int
    content: str


class IndexRequest(BaseModel):
    companyId: int
    documentId: int
    chunks: List[ChunkPayload]


@router.post("")
def index_document(
        req: IndexRequest,
):
    # (선택) 내부 호출 검증
    service.index(req)
    return {"success": True}
