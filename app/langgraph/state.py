from typing import TypedDict, Any, List

class BIState(TypedDict):
    tenant_id: str
    user_id: str
    question: str
    corrected_question: str # Added to track AI normalization
    history: List[Any]
    metadata: dict
    rag_context: str
    sql: str
    result: Any
    response: dict
