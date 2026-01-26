import hashlib
from app.infra.vector_store import VectorStore


class VectorIndexService:
    def __init__(self):
        self.store = VectorStore.get_instance()

    def index(self, req):
        for c in req.chunks:
            # Generate a deterministic point_id
            point_id_str = f"{req.companyId}-{req.documentId}-{c.chunkId}"
            point_id = int(hashlib.sha256(point_id_str.encode()).hexdigest(), 16) % (10**18) # Qdrant IDs are uin64, limit to 18 digits

            vector = self.store.embed(c.content)
            payload = {
                "companyId": req.companyId,
                "documentId": req.documentId,
                "chunkId": c.chunkId,
                "content": c.content,
            }
            self.store.add_document(point_id=point_id, vector=vector, payload=payload) # Qdrant expects string id

    async def delete_document_index(self, company_id: int, document_id: int):
        self.store.delete_points_by_document_id(document_id, company_id)
