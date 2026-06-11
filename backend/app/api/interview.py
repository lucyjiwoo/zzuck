from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import InterviewStartRequest, InterviewAnswerRequest
from app.models import (
    Answer, Feedback, InterviewSession, Question,
    QuestionType, SessionStatus, SeverityLevel, WeaknessMemory,
)
from app.services.interview_service import generate_questions, evaluate_answer

router = APIRouter(prefix="/interviews", tags=["Interviews"])


@router.post("")
def start_interview(request: InterviewStartRequest, db: Session = Depends(get_db)):
    question_texts = generate_questions(
        resume=request.resume,
        job_description=request.job_description,
        interview_type=request.interview_type,
    )

    session = InterviewSession(
        interview_type=request.interview_type,
        resume=request.resume,
        job_description=request.job_description,
        status=SessionStatus.pending,
    )
    db.add(session)
    db.flush()

    questions = []
    for i, text in enumerate(question_texts):
        q = Question(
            session_id=session.id,
            question_text=text,
            question_type=QuestionType.main,
            follow_up_depth=0,
            order_index=i,
        )
        db.add(q)
        questions.append(q)

    db.commit()

    return {
        "session_id": session.id,
        "questions": [
            {"id": q.id, "question_text": q.question_text, "type": q.question_type}
            for q in questions
        ],
    }


@router.post("/{session_id}/answers")
def submit_answer(session_id: int, request: InterviewAnswerRequest, db: Session = Depends(get_db)):
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    question = db.query(Question).filter(
        Question.id == request.question_id,
        Question.session_id == session_id,
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found in this session")

    answer = Answer(
        question_id=question.id,
        session_id=session.id,
        answer_text=request.answer,
    )
    db.add(answer)
    db.flush()

    result = evaluate_answer(
        interview_type=session.interview_type,
        question_text=question.question_text,
        answer=request.answer,
        follow_up_depth=question.follow_up_depth,
    )

    db.add(Feedback(
        answer_id=answer.id,
        session_id=session.id,
        feedback_text=result["feedback"],
        score=result["score"],
    ))

    for w in result["weaknesses"]:
        db.add(WeaknessMemory(
            session_id=session.id,
            answer_id=answer.id,
            category=w["category"],
            weakness_text=w["weakness_text"],
            severity=SeverityLevel(w["severity"]),
            evidence=request.answer,
        ))

    next_question = None
    if result["follow_up_question"]:
        next_question = Question(
            session_id=session.id,
            question_text=result["follow_up_question"],
            question_type=QuestionType.follow_up,
            parent_question_id=question.id,
            follow_up_depth=question.follow_up_depth + 1,
            order_index=len(session.questions),
        )
        db.add(next_question)
        db.flush()

    db.commit()

    return {
        "feedback": result["feedback"],
        "score": result["score"],
        "weaknesses": result["weaknesses"],
        "next_question": {
            "id": next_question.id,
            "question_text": next_question.question_text,
            "type": next_question.question_type,
        } if next_question else None,
    }


@router.get("/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session.id,
        "interview_type": session.interview_type,
        "status": session.status,
        "questions": [
            {"id": q.id, "question_text": q.question_text, "type": q.question_type}
            for q in session.questions
        ],
        "answers": [
            {"id": a.id, "question_id": a.question_id, "answer_text": a.answer_text}
            for a in session.answers
        ],
    }


@router.get("/{session_id}/feedback")
def get_feedback(session_id: int, db: Session = Depends(get_db)):
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session_id,
        "feedbacks": [
            {"answer_id": f.answer_id, "feedback_text": f.feedback_text, "score": f.score}
            for f in session.feedbacks
        ],
        "weaknesses": [
            {"category": w.category, "weakness_text": w.weakness_text, "severity": w.severity}
            for w in session.weaknesses
        ],
    }
