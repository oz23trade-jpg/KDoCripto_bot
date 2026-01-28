from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from sqlalchemy import JSON

class Quiz(SQLModel, table=True):
    __tablename__ = "quizzes"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    questions: List[dict] = Field(default_factory=list, sa_column=JSON)  # [{"q": "...", "options": [...], "correct": 2}, ...]
    daily: bool = Field(default=True)           # ежедневный или постоянный
    reward_points: int = Field(default=10)
    reward_tickets: int = Field(default=1)
    passing_score: int = Field(default=70)      # в процентах
    active_from: Optional[datetime] = None
    active_until: Optional[datetime] = None


class QuizAttempt(SQLModel, table=True):
    __tablename__ = "quiz_attempts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    quiz_id: int = Field(foreign_key="quizzes.id")
    score: int                                  # процент правильных
    answers: dict = Field(default_factory=dict, sa_column=JSON)  # {q_index: selected_option}
    awarded_points: int = Field(default=0)
    awarded_tickets: int = Field(default=0)
    completed_at: datetime = Field(default_factory=datetime.utcnow)