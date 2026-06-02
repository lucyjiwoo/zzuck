from fastapi import APIRouter
from app.services.openai_client import client


router = APIRouter()

@router.get("/openai")
def ask_openai(question: str):

    response = client.responses.create(
        model="gpt-4.1-nano",
        input=question
    )

    return {"message": response.output_text}