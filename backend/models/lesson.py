# backend/models/lesson.py
from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Index


class Course(SQLModel, table=True):
    __tablename__ = "courses"
    __table_args__ = (
        Index("ix_course_order", "order"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    order: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime, onupdate=datetime.utcnow))


class Lesson(SQLModel, table=True):
    __tablename__ = "lessons"
    __table_args__ = (
        Index("ix_lesson_course_order", "course_id", "lesson_order"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id")
    title: str
    content: str                            # markdown или plain text
    lesson_order: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserLessonProgress(SQLModel, table=True):
    __tablename__ = "user_lesson_progress"
    __table_args__ = (
        Index("ix_user_lesson_progress_user", "user_id"),
    )

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    lesson_id: int = Field(foreign_key="lessons.id", primary_key=True)
    completed: bool = Field(default=False)
    completed_at: Optional[datetime] = None
    score: Optional[int] = None             # если будет тест в уроке
