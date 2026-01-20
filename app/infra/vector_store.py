import chromadb
from chromadb.utils import embedding_functions
from app.core.settings import settings

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=settings.OPENAI_API_KEY,
    model_name="text-embedding-3-small",
)

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="hradar_policy",
            embedding_function=openai_ef,
        )

    def search(self, query: str, top_k: int = 3) -> list[str]:
        res = self.collection.query(
            query_texts=[query],
            n_results=top_k,
        )
        return res.get("documents", [[]])[0]
