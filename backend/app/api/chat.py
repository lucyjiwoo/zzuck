from fastapi import APIRouter
from app.services.openai_client import get_openai_client

router = APIRouter()

@router.get("/openai")

def ask_openai(question: str):
    client = get_openai_client()
    response = client.responses.create(
        model="gpt-4.1-nano",
        input=question
    )

    return {"message": response.output_text}