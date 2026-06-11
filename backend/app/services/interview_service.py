import json

from app.services.openai_client import get_openai_client

_MODEL = "gpt-4.1-nano"
MAX_FOLLOW_UP_DEPTH = 2


def generate_questions(resume: str, job_description: str, interview_type: str) -> list[str]:
    """Returns a list of question strings. IDs are assigned by the DB after insertion."""
    client = get_openai_client()

    response = client.responses.create(
        model=_MODEL,
        input=f"""
You are an interview coach.

Interview type: {interview_type}

Resume:
{resume}

Job Description:
{job_description}

Generate 3 personalized interview questions.

Return ONLY valid JSON in this exact format:
{{
  "questions": ["question 1", "question 2", "question 3"]
}}
""",
    )

    return json.loads(response.output_text)["questions"]


def evaluate_answer(
    interview_type: str,
    question_text: str,
    answer: str,
    follow_up_depth: int,
) -> dict:
    """
    Returns:
      feedback, score (0.0–1.0), weaknesses [{weakness_text, category, severity}],
      follow_up_question (None if max depth reached)
    """
    client = get_openai_client()

    response = client.responses.create(
        model=_MODEL,
        input=f"""
You are an interview coach.

Interview type: {interview_type}

Question:
{question_text}

Candidate answer:
{answer}

Evaluate the answer and return ONLY valid JSON in this exact format:
{{
  "feedback": "clear and constructive feedback",
  "score": 0.75,
  "weaknesses": [
    {{
      "weakness_text": "specific weakness description",
      "category": "e.g. problem solving, communication, system design, algorithms",
      "severity": "low"
    }}
  ],
  "follow_up_question": "one adaptive follow-up question"
}}

Rules:
- score: float between 0.0 and 1.0
- severity: one of low, medium, high
- weaknesses: empty list if the answer is strong
- always include a follow_up_question
""",
    )

    result = json.loads(response.output_text)

    return {
        "feedback": result["feedback"],
        "score": float(result["score"]),
        "weaknesses": result["weaknesses"],
        "follow_up_question": result["follow_up_question"] if follow_up_depth < MAX_FOLLOW_UP_DEPTH else None,
    }
