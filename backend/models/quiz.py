# backend/models/quiz.py
from typing import Optional, List, Dict
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import JSON, Index


class Quiz(SQLModel, table=True):
    """
    Квиз (ежедневный или постоянный).
    Хранит вопросы в JSON-формате.
    """

    __tablename__ = "quizzes"
    __table_args__ = (
        Index("ix_quiz_daily_active", "daily", "active_from", "active_until"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)
    questions: List[Dict] = Field(
        default_factory=list,
        sa_column=JSON,
        description='[{"q": "Вопрос", "options": ["A", "B", "C"], "correct": 1}, ...]'
    )
    daily: bool = Field(default=True, index=True, description="Ежедневный квиз (true) или постоянный")
    reward_points: int = Field(default=10)
    reward_tickets: int = Field(default=1)
    passing_score: int = Field(default=70, description="Процент для прохождения")
    active_from: Optional[datetime] = Field(default=None)
    active_until: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class QuizAttempt(SQLModel, table=True):
    """
    Попытка прохождения квиза пользователем.
    """

    __tablename__ = "quiz_attempts"
    __table_args__ = (
        Index("ix_quiz_attempt_user_quiz", "user_id", "quiz_id"),
        Index("ix_quiz_attempt_completed", "completed_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    quiz_id: int = Field(foreign_key="quizzes.id", index=True)
    score: int = Field(description="Процент правильных ответов")
    answers: Dict = Field(
        default_factory=dict,
        sa_column=JSON,
        description='{0: 1, 1: 0, ...} — индекс вопроса → выбранный вариант'
    )
    awarded_points: int = Field(default=0)
    awarded_tickets: int = Field(default=0)
    is_completed: bool = Field(default=False, index=True)
    completed_at: Optional[datetime] = Field(default=None)
