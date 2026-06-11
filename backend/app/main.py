from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.chat import router as chat_router
from app.api.interview import router as interview_router
from app.models import Base
from app.db.session import engine

# Create all tables on startup. Replace with Alembic migrations before production.
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(interview_router)
