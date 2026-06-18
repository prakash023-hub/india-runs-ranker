"""Job-description signals for Senior AI Engineer @ Redrob."""

from __future__ import annotations

# Core technical keywords — weighted by JD emphasis
CORE_SKILLS: dict[str, float] = {
    "python": 2.5,
    "embedding": 4.0,
    "embeddings": 4.0,
    "retrieval": 4.5,
    "information retrieval": 4.5,
    "ranking": 4.5,
    "learning to rank": 4.0,
    "rag": 3.5,
    "vector search": 4.0,
    "vector": 2.5,
    "llm": 2.5,
    "llms": 2.5,
    "fine-tuning": 2.5,
    "fine tuning": 2.5,
    "fine-tuning llms": 3.0,
    "lora": 2.0,
    "qlora": 2.0,
    "sentence-transformer": 3.0,
    "sentence transformer": 3.0,
    "faiss": 3.0,
    "pgvector": 3.0,
    "elasticsearch": 2.5,
    "opensearch": 2.5,
    "pinecone": 2.5,
    "weaviate": 2.0,
    "qdrant": 2.0,
    "milvus": 2.0,
    "xgboost": 2.0,
    "ndcg": 3.0,
    "mrr": 2.5,
    "hybrid search": 3.5,
    "recommendation system": 3.5,
    "recommendation engine": 3.5,
    "nlp": 2.0,
    "pytorch": 2.5,
    "tensorflow": 1.5,
    "production": 3.0,
    "deployed": 2.5,
    "deployment": 2.5,
    "a/b test": 2.0,
    "offline benchmark": 2.0,
}

# Strong title matches for this JD
TITLE_STRONG: dict[str, float] = {
    "senior ai engineer": 12.0,
    "lead ai engineer": 11.0,
    "staff ai engineer": 10.0,
    "ai engineer": 9.0,
    "senior machine learning engineer": 11.0,
    "staff machine learning engineer": 10.0,
    "machine learning engineer": 9.0,
    "ml engineer": 9.0,
    "applied ml engineer": 8.0,
    "senior ml engineer": 10.0,
}

TITLE_MILD: dict[str, float] = {
    "data scientist": 3.0,
    "applied scientist": -4.0,
    "research scientist": -6.0,
    "ai research engineer": -3.0,
    "research engineer": -4.0,
    "backend engineer": 2.0,
    "software engineer": 2.5,
    "data engineer": 3.0,
    "platform engineer": 2.0,
}

# Keyword-stuffing trap titles (JD explicit)
TITLE_TRAP: set[str] = {
    "marketing manager",
    "hr manager",
    "content writer",
    "graphic designer",
    "sales executive",
    "accountant",
    "customer support",
    "civil engineer",
    "mechanical engineer",
    "business analyst",
    "operations manager",
    "project manager",
}

CAREER_PRODUCTION_PHRASES: dict[str, float] = {
    "production": 3.0,
    "deployed": 3.0,
    "deployment": 2.5,
    "shipped": 2.5,
    "recommendation": 3.0,
    "ranking": 3.5,
    "retrieval": 3.5,
    "embedding": 3.0,
    "vector search": 3.5,
    "hybrid search": 3.5,
    "a/b test": 2.5,
    "recruiter": 2.0,
    "candidate matching": 2.5,
    "search infrastructure": 3.0,
    "feature pipeline": 2.0,
    "model serving": 2.5,
    "inference": 2.0,
    "index refresh": 2.5,
    "learning to rank": 3.5,
}

NEGATIVE_PHRASES: tuple[str, ...] = (
    "langchain only",
    "research only",
    "academic lab",
    "pure research",
    "thesis work",
    "published papers only",
    "no production",
)

IDEAL_EXP_MIN = 5.0
IDEAL_EXP_MAX = 9.0
EXP_ACCEPT_MIN = 4.0
EXP_ACCEPT_MAX = 11.0


def experience_score(years: float) -> float:
    if years < 3.0:
        return 0.1
    if IDEAL_EXP_MIN <= years <= IDEAL_EXP_MAX:
        return 1.0
    if EXP_ACCEPT_MIN <= years < IDEAL_EXP_MIN:
        return 0.55 + 0.1 * (years - EXP_ACCEPT_MIN)
    if IDEAL_EXP_MAX < years <= EXP_ACCEPT_MAX:
        return max(0.35, 1.0 - 0.12 * (years - IDEAL_EXP_MAX))
    if years > EXP_ACCEPT_MAX:
        return max(0.05, 0.35 - 0.04 * (years - EXP_ACCEPT_MAX))
    return 0.25
