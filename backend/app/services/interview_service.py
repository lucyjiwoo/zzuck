import json

from app.services.openai_client import get_openai_client

_MODEL = "gpt-4.1-nano"
MAX_FOLLOW_UP_DEPTH = 2


def generate_questions(
    resume: str,
    job_description: str,
    interview_type: str,
) -> list[dict]:
    """
    Generate initial interview questions based on the candidate's resume,
    job description, and interview type.

    Returns a list of question dicts ready to be stored in the session.
    """
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
  "questions": [
    "question 1",
    "question 2",
    "question 3"
  ]
}}
""",
    )

    result = json.loads(response.output_text)

    return [
        {
            "id": f"q{i + 1}",
            "question": q,
            "type": "main",
            "parent_question_id": None,
            "follow_up_depth": 0,
        }
        for i, q in enumerate(result["questions"])
    ]


def evaluate_answer(
    session: dict,
    current_question: dict,
    answer: str,
) -> dict:
    """
    Evaluate a candidate's answer for a given question.

    Returns a dict with:
      - feedback:          str
      - weaknesses:        list[str]
      - follow_up_question: str | None  (None if max depth reached)
    """
    client = get_openai_client()

    response = client.responses.create(
        model=_MODEL,
        input=f"""
You are an interview coach.

Interview type: {session["interview_type"]}

Question:
{current_question["question"]}

User answer:
{answer}

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
""",
    )

    result = json.loads(response.output_text)

    should_follow_up = current_question["follow_up_depth"] < MAX_FOLLOW_UP_DEPTH

    return {
        "feedback": result["feedback"],
        "weaknesses": result["weaknesses"],
        "follow_up_question": result["follow_up_question"] if should_follow_up else None,
    }
