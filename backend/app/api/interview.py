import json
import uuid

from fastapi import APIRouter, HTTPException

from app.models import InterviewStartRequest, InterviewAnswerRequest
from app.temp_memory import INTERVIEW_SESSIONS
from app.services.openai_client import get_openai_client


router = APIRouter(prefix="/interview", tags=["Interview"])

MAX_FOLLOW_UP_DEPTH = 2


@router.post("/start")
def start_interview(request: InterviewStartRequest):
    client = get_openai_client()
    prompt = f"""
You are an interview coach.

Interview type: {request.interview_type}

Resume:
{request.resume}

Job Description:
{request.job_description}

Generate 3 personalized interview questions.

Return ONLY valid JSON in this exact format:
{{
  "questions": [
    "question 1",
    "question 2",
    "question 3"
  ]
}}
"""

    response = client.responses.create(
        model="gpt-4.1-nano",
        input=prompt,
    )

    try:
        result = json.loads(response.output_text)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to parse OpenAI response as JSON"
        )

    session_id = str(uuid.uuid4())

    questions = [
        {
            "id": f"q{i + 1}",
            "question": question,
            "type": "main",
            "parent_question_id": None,
            "follow_up_depth": 0,
        }
        for i, question in enumerate(result["questions"])
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
def answer_interview(request: InterviewAnswerRequest):
    client = get_openai_client()
    session = INTERVIEW_SESSIONS.get(request.session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    current_question = next(
        (
            question for question in session["questions"]
            if question["id"] == request.question_id
        ),
        None,
    )

    if not current_question:
        raise HTTPException(status_code=404, detail="Question not found")

    should_generate_follow_up = (
        current_question["follow_up_depth"] < MAX_FOLLOW_UP_DEPTH
    )

    prompt = f"""
You are an interview coach.

Interview type: {session["interview_type"]}

Question:
{current_question["question"]}

User answer:
{request.answer}

Evaluate the answer.

Return ONLY valid JSON in this exact format:
{{
  "feedback": "clear feedback as a string",
  "weaknesses": [
    "weakness 1",
    "weakness 2"
  ],
  "follow_up_question": "one adaptive follow-up question"
}}

If the answer is already strong, still provide one useful follow-up question.
"""

    response = client.responses.create(
        model="gpt-4.1-nano",
        input=prompt,
    )

    try:
        result = json.loads(response.output_text)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to parse OpenAI response as JSON"
        )

    answer_record = {
        "question_id": request.question_id,
        "answer": request.answer,
        "feedback": result["feedback"],
        "weaknesses": result["weaknesses"],
    }

    session["answers"].append(answer_record)
    session["weaknesses"].extend(result["weaknesses"])

    next_question = None

    if should_generate_follow_up:
        next_question = {
            "id": f"q{len(session['questions']) + 1}",
            "question": result["follow_up_question"],
            "type": "follow_up",
            "parent_question_id": request.question_id,
            "follow_up_depth": current_question["follow_up_depth"] + 1,
        }

        session["questions"].append(next_question)

    return {
        "feedback": result["feedback"],
        "weaknesses": result["weaknesses"],
        "next_question": next_question,
    }