from app.infra.vector_store import VectorStore


class VectorIndexService:
    def __init__(self):
        self.store = VectorStore()

    def index(self, req):
        for c in req.chunks:
            self.store.add_document({
                "companyId": req.companyId,
                "documentId": req.documentId,
                "chunkId": c.chunkId,
                "content": c.content
            })
