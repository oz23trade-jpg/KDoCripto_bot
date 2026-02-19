# backend/models/__init__.py

from sqlmodel import SQLModel

# ── Основные модели ─────────────────
from .user import User
from .admin_log import AdminActionLog
from .referral import Referral

# ── Обучение ─────────────────
from .lesson import Course, Lesson, UserLessonProgress

# ── Квизы ─────────────────
from .quiz import Quiz, QuizAttempt

# ── Лотерея ─────────────────
from .lottery import LotteryDraw, LotteryTicket

# ── Платежи ─────────────────
from .payment import Payment


__all__ = [
    "SQLModel",
    "User",
    "AdminActionLog",
    "Referral",
    "Course",
    "Lesson",
    "UserLessonProgress",
    "Quiz",
    "QuizAttempt",
    "LotteryDraw",
    "LotteryTicket",
    "Payment",
]
