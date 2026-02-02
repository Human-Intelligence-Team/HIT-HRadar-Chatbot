import uuid
from typing import Union
from app.infra.vector_store import VectorStore


class VectorIndexService:
    def __init__(self):
        self.store = VectorStore.get_instance()

    def index(self, req):
        for c in req.chunks:
            # Match the point ID logic with DocumentService (valid UUID strings)
            point_id = str(uuid.uuid4())

            vector = self.store.embed(c.content)
            payload = {
                "companyId": req.companyId,
                "documentId": req.documentId,
                "chunkId": c.chunkId,
                "title": c.title if c.title else (req.title if req.title else "Untitled"),
                "content": c.content,
            }
            self.store.add_document(point_id=point_id, vector=vector, payload=payload)

    def delete_document_index(self, company_id: int, document_id: Union[int, str]):
        self.store.delete_points_by_document_id(document_id, company_id)
