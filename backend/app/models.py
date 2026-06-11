import enum
from datetime import datetime

from sqlalchemy import ForeignKey, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector


class Base(DeclarativeBase):
    pass


# ── Enums ────────────────────────────────────────────────────────────────────

class InterviewType(str, enum.Enum):
    technical = "technical"
    behavioral = "behavioral"
    coding = "coding"


class SessionStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class QuestionType(str, enum.Enum):
    main = "main"
    follow_up = "follow_up"


class SeverityLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class WeaknessStatus(str, enum.Enum):
    active = "active"
    resolved = "resolved"


# ── Models ───────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None]
    email: Mapped[str | None] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    interview_type: Mapped[InterviewType]
    resume: Mapped[str] = mapped_column(Text)
    job_description: Mapped[str] = mapped_column(Text)
    status: Mapped[SessionStatus] = mapped_column(default=SessionStatus.pending)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    completed_at: Mapped[datetime | None]

    questions: Mapped[list["Question"]] = relationship(
        back_populates="session", order_by="Question.order_index"
    )
    answers: Mapped[list["Answer"]] = relationship(back_populates="session")
    feedbacks: Mapped[list["Feedback"]] = relationship(back_populates="session")
    weaknesses: Mapped[list["WeaknessMemory"]] = relationship(back_populates="session")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id"))
    question_text: Mapped[str] = mapped_column(Text)
    question_type: Mapped[QuestionType]
    parent_question_id: Mapped[int | None] = mapped_column(ForeignKey("questions.id"))
    follow_up_depth: Mapped[int] = mapped_column(default=0)
    order_index: Mapped[int]

    session: Mapped["InterviewSession"] = relationship(back_populates="questions")
    answers: Mapped[list["Answer"]] = relationship(back_populates="question")


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id"))
    answer_text: Mapped[str] = mapped_column(Text)
    embedding_vector: Mapped[list | None] = mapped_column(Vector(1536))  # populated in Phase 4
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    session: Mapped["InterviewSession"] = relationship(back_populates="answers")
    question: Mapped["Question"] = relationship(back_populates="answers")
    feedback: Mapped["Feedback | None"] = relationship(back_populates="answer", uselist=False)
    weaknesses: Mapped[list["WeaknessMemory"]] = relationship(back_populates="answer")


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(primary_key=True)
    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id"))
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id"))
    feedback_text: Mapped[str] = mapped_column(Text)
    score: Mapped[float]  # 0.0 – 1.0
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    answer: Mapped["Answer"] = relationship(back_populates="feedback")
    session: Mapped["InterviewSession"] = relationship(back_populates="feedbacks")


class WeaknessMemory(Base):
    __tablename__ = "weakness_memory"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))  # nullable until auth is added
    session_id: Mapped[int] = mapped_column(ForeignKey("interview_sessions.id"))
    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id"))
    category: Mapped[str]
    weakness_text: Mapped[str] = mapped_column(Text)
    severity: Mapped[SeverityLevel]
    evidence: Mapped[str | None] = mapped_column(Text)
    embedding_vector: Mapped[list | None] = mapped_column(Vector(1536))  # populated in Phase 4
    last_seen_at: Mapped[datetime] = mapped_column(server_default=func.now())
    status: Mapped[WeaknessStatus] = mapped_column(default=WeaknessStatus.active)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    answer: Mapped["Answer"] = relationship(back_populates="weaknesses")
    session: Mapped["InterviewSession"] = relationship(back_populates="weaknesses")
