# backend/models/__init__.py
"""
Экспорт всех SQLModel-моделей проекта для удобного импорта в одном месте.

Пример использования:
    from models import User, Referral, Quiz

Все новые модели добавляй сюда после создания файла модели.
"""

# ── Основные модели ────────────────────────────────────────────────────────
from .user import User
from .admin_log import AdminActionLog
from .referral import Referral

# ── Обучение и квизы ───────────────────────────────────────────────────────
from .lesson import Lesson, Course, UserLessonProgress
from .quiz import Quiz, QuizAttempt

# ── Лотерея и платежи (раскомментируй при создании) ────────────────────────
# from .lottery import LotteryDraw, LotteryTicket
# from .payment import Payment

# ── Экспортируемые имена (для from models import *) ────────────────────────
__all__ = [
    # Пользователи и админ
    "User",
    "AdminActionLog",
    "Referral",
    
    # Обучение
    "Course",
    "Lesson",
    "UserLessonProgress",
    
    # Квизы
    "Quiz",
    "QuizAttempt",
    
    # Будущие модели (добавляй сюда по мере создания)
    # "LotteryDraw",
    # "LotteryTicket",
    # "Payment",
]
