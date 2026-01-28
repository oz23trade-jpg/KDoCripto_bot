from pydantic import BaseModel
from typing import Optional, List, Dict


# ==================== User schemas ====================
class UserCreate(BaseModel):
    id: int
    lang: str = "en"
    username: Optional[str] = None
    name: Optional[str] = None
    referrer_id: Optional[int] = None


class UserUpdate(BaseModel):
    lang: Optional[str] = None
    username: Optional[str] = None
    name: Optional[str] = None


class UserOut(BaseModel):
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
class LanguageUpdate(BaseModel):
    lang: str  # en/ru/fi


class PointsGrant(BaseModel):
    user_id: int
    points: int
    reason: str


class TicketGrant(BaseModel):
    user_id: int
    tickets: int = 1
    source: str  # daily/quiz/referral/donate


# ==================== Learning & Quiz schemas ====================
class LessonComplete(BaseModel):
    user_id: int
    lesson_id: int


class QuizAnswer(BaseModel):
    quiz_id: int
    question_idx: int
    option_idx: int


class QuizResult(BaseModel):
    score: int          # процент правильных ответов
    passed: bool
    awarded_points: int
    ticket_granted: bool