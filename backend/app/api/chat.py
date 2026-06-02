from fastapi import APIRouter
from openai import OpenAI
from app.config import OPENAI_API_KEY

router = APIRouter()

@router.get("/openai")
def ask_openai(question: str):
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.responses.create(
        model="gpt-4.1-nano",
        input=question
    )

    return {"message": response.output_text}