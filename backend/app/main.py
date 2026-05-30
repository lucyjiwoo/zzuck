from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from openai import OpenAI
import os



client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/openai")
def ask(question: str):
    response = client.responses.create(
        model="gpt-4.1-nano",
        input=question
    )

    return {
        "message": response.output_text
    }