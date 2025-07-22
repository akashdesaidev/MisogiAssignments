from fastapi import APIRouter
from pydantic import BaseModel
# from services.embedder import embed_query
# from services.retriever import retrieve_chunks
# from services.llm import generate_answer

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 4

@router.post("/query")
async def ask_question(request: QueryRequest):
    # query_embedding = embed_query(request.query)
    # chunks = retrieve_chunks(query_embedding, k=request.top_k)
    # chunk_texts = [chunk["document"] for chunk in chunks]

    # answer = generate_answer(request.query, chunk_texts)
    return {
        "question": request.query,
        "answer": "answer",
        "contexts": "contexts"
    }