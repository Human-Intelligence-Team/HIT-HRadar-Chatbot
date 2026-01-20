from app.infra.vector_store import VectorStore

docs = [
    {
        "id": "policy_eval_1",
        "text": "평가 제도는 연 1회 실시되며 역량 평가와 성과 평가로 구성됩니다.",
        "meta": {"type": "POLICY_EVALUATION"},
    },
    {
        "id": "policy_eval_2",
        "text": "평가 결과는 승진, 보상, 인사 배치에 반영됩니다.",
        "meta": {"type": "POLICY_EVALUATION"},
    },
    {
        "id": "policy_comp_1",
        "text": "역량은 직무 수행에 필요한 지식, 기술, 태도를 의미합니다.",
        "meta": {"type": "POLICY_COMPETENCY"},
    },
]

store = VectorStore()
store.add_documents(docs)

print("✅ 정책 문서 적재 완료")
