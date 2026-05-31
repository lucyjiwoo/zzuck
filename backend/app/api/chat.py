from fastapi import APIRouter
from openai import OpenAI

router = APIRouter()

client = OpenAI()

@router.post("/chat")
def chat(question: str):
    response = client.responses.create(
        model="gpt-4.1-nano",
        input=question
    )

    return {
        "message": response.output_text
    }