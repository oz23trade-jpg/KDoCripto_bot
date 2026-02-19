# backend/schemas.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Literal


# ==================== User schemas ====================

class UserCreate(BaseModel):
    id: int
    lang: Literal["en", "ru", "fi"] = "en"
    username: Optional[str] = None
    name: Optional[str] = None
    referrer_id: Optional[int] = None


class UserUpdate(BaseModel):
    lang: Optional[Literal["en", "ru", "fi"]] = None
    username: Optional[str] = None
    name: Optional[str] = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lang: str
    username: Optional[str] = None
    name: Optional[str] = None
    points: int
    xp: int
    level: int
    referrals_count: int
    tickets: int
    badges: Optional[List[dict]] = None
    settings: Optional[Dict[str, dict]] = None


# ==================== Admin / Reward schemas ====================

class PointsGrant(BaseModel):
    user_id: int
    points: int = Field(..., ge=1)
    reason: str


class TicketGrant(BaseModel):
    user_id: int
    tickets: int = Field(default=1, ge=1)
    source: str


# ==================== Learning & Quiz schemas ====================

class LessonComplete(BaseModel):
    user_id: int
    lesson_id: int


class QuizAnswer(BaseModel):
    quiz_id: int
    question_idx: int
    option_idx: int


class QuizResult(BaseModel):
    score: int = Field(..., ge=0, le=100)
    passed: bool
    awarded_points: int
    ticket_granted: bool
