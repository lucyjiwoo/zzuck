from pydantic import BaseModel
from typing import Literal


class InterviewStartRequest(BaseModel):
    interview_type: Literal["coding", "technical", "behavioral"]
    resume: str
    job_description: str


class InterviewAnswerRequest(BaseModel):
    # session_id comes from the URL path, not the request body
    question_id: int
    answer: str
