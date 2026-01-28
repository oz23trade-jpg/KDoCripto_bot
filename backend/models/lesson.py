from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Course(SQLModel, table=True):
    __tablename__ = "courses"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    order: int = Field(default=0)


class Lesson(SQLModel, table=True):
    __tablename__ = "lessons"

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id")
    title: str
    content: str                            # markdown или plain text
    lesson_order: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserLessonProgress(SQLModel, table=True):
    __tablename__ = "user_lesson_progress"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    lesson_id: int = Field(foreign_key="lessons.id", primary_key=True)
    completed: bool = Field(default=False)
    completed_at: Optional[datetime] = None
    score: Optional[int] = None             # если будет тест в уроке