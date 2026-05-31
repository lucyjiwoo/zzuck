from fastapi import FastAPI
from app.api.chat import router as chat_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(chat_router)