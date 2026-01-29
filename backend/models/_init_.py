# backend/models/__init__.py
"""
Экспорт всех моделей для удобного импорта:
    from models import User, AdminActionLog, Lesson, ...
"""

# Импортируем модели из отдельных файлов
from .user import User
from .admin_log import AdminActionLog
from .lesson import Lesson, Course, UserLessonProgress
from .quiz import Quiz, QuizAttempt
from .referral import Referral

# Другие модели (добавляй по мере создания)
# from .lottery import LotteryDraw, LotteryTicket
# from .payment import Payment

# Список всех экспортируемых имён (для удобства: from models import *)
__all__ = [
    "User",
    "AdminActionLog",
    "Lesson",
    "Course",
    "UserLessonProgress",
    "Quiz",
    "QuizAttempt",
    "Referral",
    # Добавляй новые модели сюда
    # "LotteryDraw",
    # "LotteryTicket",
    # "Payment",
]
