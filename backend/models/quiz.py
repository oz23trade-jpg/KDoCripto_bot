from typing import Optional, List, Dict
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON, Index


class Quiz(SQLModel, table=True):

    __tablename__ = "quizzes"
    __table_args__ = (
        Index("ix_quiz_daily_active", "daily", "active_from", "active_until"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)

    questions: List[Dict] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False)
    )

    daily: bool = Field(default=True, index=True)
    reward_points: int = Field(default=10)
    reward_tickets: int = Field(default=1)
    passing_score: int = Field(default=70)

    active_from: Optional[datetime] = None
    active_until: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)


class QuizAttempt(SQLModel, table=True):

    __tablename__ = "quiz_attempts"
    __table_args__ = (
        Index("ix_quiz_attempt_user_quiz", "user_id", "quiz_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id", index=True)
    quiz_id: int = Field(foreign_key="quizzes.id", index=True)

    score: int

    answers: Dict = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=False)
    )

    awarded_points: int = Field(default=0)
    awarded_tickets: int = Field(default=0)

    is_completed: bool = Field(default=False)
    completed_at: Optional[datetime] = None
