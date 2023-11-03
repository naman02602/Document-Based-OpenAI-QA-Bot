from fastapi import APIRouter, Depends
from routers.authentication import get_current_user
from fastapi_service import models
from module import generate_embedding, pinecone_queries, generate_answer
import pinecone

router = APIRouter(tags=["dummy"])

@router.post("/ask")
async def ask_question(
    question: models.Question, user: dict = Depends(get_current_user)
):
    embedding = generate_embedding.generate_embedding(question.question)
    top_k = 1  # You can adjust this value based on your requirements

    pinecone_results = pinecone_queries.query_pinecone(
        embedding, top_k, selected_pdfs=question.pdfs
    )

    print(pinecone_results)
    query = pinecone_queries.format_query(
        question.question, pinecone_results["matches"]
    )
    print(query)

    answer = generate_answer.generate_answer(query)

    return {"answer": answer}
