import uuid

from fastapi import APIRouter, HTTPException

from app.models import InterviewStartRequest, InterviewAnswerRequest
from app.temp_memory import INTERVIEW_SESSIONS
from app.services.interview_service import generate_questions, evaluate_answer

router = APIRouter(prefix="/interviews", tags=["Interviews"])


@router.post("")
def start_interview(request: InterviewStartRequest):
    """Start a new interview session and return the initial questions."""
    questions = generate_questions(
        resume=request.resume,
        job_description=request.job_description,
        interview_type=request.interview_type,
    )

    session_id = str(uuid.uuid4())
    INTERVIEW_SESSIONS[session_id] = {
        "interview_type": request.interview_type,
        "resume": request.resume,
        "job_description": request.job_description,
        "questions": questions,
        "answers": [],
        "weaknesses": [],
    }

    return {"session_id": session_id, "questions": questions}


@router.post("/{session_id}/answers")
def submit_answer(session_id: str, request: InterviewAnswerRequest):
    """Submit an answer for a question and receive feedback + optional follow-up."""
    session = INTERVIEW_SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    current_question = next(
        (q for q in session["questions"] if q["id"] == request.question_id),
        None,
    )
    if not current_question:
        raise HTTPException(status_code=404, detail="Question not found")

    result = evaluate_answer(
        session=session,
        current_question=current_question,
        answer=request.answer,
    )

    session["answers"].append({
        "question_id": request.question_id,
        "answer": request.answer,
        "feedback": result["feedback"],
        "weaknesses": result["weaknesses"],
    })
    session["weaknesses"].extend(result["weaknesses"])

    next_question = None
    if result["follow_up_question"]:
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


@router.get("/{session_id}")
def get_session(session_id: str):
    """Return the current state of an interview session."""
    session = INTERVIEW_SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session_id,
        "interview_type": session["interview_type"],
        "questions": session["questions"],
        "answers": session["answers"],
    }


@router.get("/{session_id}/feedback")
def get_feedback(session_id: str):
    """Return aggregated feedback and identified weaknesses for a session."""
    session = INTERVIEW_SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session_id,
        "weaknesses": session["weaknesses"],
        "answers": [
            {
                "question_id": a["question_id"],
                "feedback": a["feedback"],
            }
            for a in session["answers"]
        ],
    }
