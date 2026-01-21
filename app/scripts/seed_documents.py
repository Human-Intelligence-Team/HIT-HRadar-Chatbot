from app.infra.vector_store import VectorStore

vector = VectorStore()

docs = [
    {
        "id": "leave_001",
        "title": "연차 기준",
        "content": "연차는 발생일 기준 1년간 사용 가능하며 미사용 시 소멸됩니다.",
        "category": "POLICY",
    }
]

for d in docs:
    vector.add_document(d)

print("✅ documents seeded")
