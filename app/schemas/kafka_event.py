from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class DocumentIndexEventType(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class VectorChunkRequest(BaseModel):
    chunk_id: int = Field(..., alias="chunkId")
    title: Optional[str] = None
    content: str


class DocumentIndexEvent(BaseModel):
    event_id: str = Field(..., alias="eventId")
    company_id: int = Field(..., alias="companyId")
    document_id: int = Field(..., alias="documentId")
    title: Optional[str] = None
    type: DocumentIndexEventType
    chunks: Optional[List[VectorChunkRequest]] = None

    model_config = ConfigDict(populate_by_name=True)
