# backend/models/__init__.py
"""
Экспорт всех моделей для удобного импорта:
    from models import User, AdminActionLog, Lesson, ...
"""

from .user import User
from .admin_log import AdminActionLog
from .lesson import Lesson, Course, UserLessonProgress
from .quiz import Quiz, QuizAttempt
from .referral import Referral

# Другие модели (добавляй по мере создания)
# from .lottery import LotteryDraw, LotteryTicket
# from .payment import Payment

__all__ = [
    "AdminActionLog",
    "Course",
    "Lesson",
    "Quiz",
    "QuizAttempt",
    "Referral",
    "User",
    "UserLessonProgress",
    # Добавляй новые модели сюда
    # "LotteryDraw",
    # "LotteryTicket",
    # "Payment",
]
