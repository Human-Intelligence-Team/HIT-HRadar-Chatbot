import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
from app.core.settings import settings


class VectorStore:
    def __init__(self):
        # 로컬 embedding 모델
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )

        self.collection = settings.QDRANT_COLLECTION
        self._ensure_collection()

    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection for c in collections):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=384,  # all-MiniLM-L6-v2
                    distance=Distance.COSINE,
                ),
            )

    def embed(self, text: str) -> list[float]:
        return self.embedder.encode(text).tolist()

    def add_document(self, doc: dict):
        vector = self.embed(doc["content"])

        self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload=doc,
                )
            ],
        )

    def search(self, query: str, limit: int = 3) -> list[dict]:
        query_vector = self.embed(query)

        hits = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=limit,
        )

        return [h.payload for h in hits]
