import uuid
from fastapi import APIRouter
from app.services.openai_client import client

from app.models import InterviewStartRequest, InterviewAnswerRequest
from app.temp_memory import INTERVIEW_SESSIONS

router = APIRouter(prefix="/interview", tags=["Interview"])

@router.post("/start")
def start_interview(request: InterviewStartRequest):
    prompt = f"""
                You are an interview coach.

                Interview type: {request.interview_type}

                Resume:
                {request.resume}

                Job Description:
                {request.job_description}

                Generate 3 personalized interview questions.
                Return only the questions as a numbered list.
                """
    response = client.responses.create(
        model="gpt-4.1-nano",
        input=prompt,
    )
    questions_text = response.output_text

    session_id = str(uuid.uuid4())

    questions = [
        {"id": f"q{i+1}", "question": q.strip()}
        for i, q in enumerate(questions_text.split("\n"))
        if q.strip()
    ]
    INTERVIEW_SESSIONS[session_id] = {
        "interview_type": request.interview_type,
        "resume": request.resume,
        "job_description": request.job_description,
        "questions": questions,
        "answers": [],
        "weaknesses": [],
    }

    return {
        "session_id": session_id,
        "questions": questions,
    }

@router.post("/answer")
def answer_question(request: InterviewAnswerRequest):
    session = INTERVIEW_SESSIONS.get(request.session_id)
    if not session:
        return {"error": "Invalid session ID"}

    prompt = f"""
                You are an interview coach.

                Interview type: {session["interview_type"]}

                Question ID:
                {request.question_id}

                User answer:
                {request.answer}

                Evaluate the answer.
                Return:
                1. Feedback
                2. Weaknesses
                3. One adaptive follow-up question
                """

    response = client.responses.create(
        model="gpt-4.1-nano",
        input=prompt,
    )

    feedback_text = response.output_text

    session["answers"].append({
        "question_id": request.question_id,
        "answer": request.answer,
        "feedback": feedback_text,
    })

    return {
        "feedback": feedback_text,
        "follow_up_question": "See feedback above for adaptive follow-up question."
    }