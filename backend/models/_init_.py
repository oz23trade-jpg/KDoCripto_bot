# backend/models/__init__.py
"""
Экспорт всех моделей для удобного импорта:
    from models import User, AdminActionLog, ...
"""

# Список всех моделей, которые уже созданы или будут созданы
from .user import User
from .admin_log import AdminActionLog

# Добавляй сюда новые модели по мере создания файлов
# from .lesson import Lesson, Course, UserLessonProgress
# from .quiz import Quiz, QuizAttempt
# from .lottery import LotteryDraw, LotteryTicket
# from .payment import Payment
# from .referral import Referral

# Опционально: список всех экспортируемых имён (для from models import *)
__all__ = [
    "User",
    "AdminActionLog",
    # Добавляй новые модели сюда, когда они появятся
    # "Lesson", "Course", "UserLessonProgress",
    # "Quiz", "QuizAttempt",
    # "LotteryDraw", "LotteryTicket",
    # "Payment",
    # "Referral",
]from .lesson import Lesson, Course, UserLessonProgress
from .quiz import Quiz, QuizAttempt

__all__.extend(["Lesson", "Course", "UserLessonProgress", "Quiz", "QuizAttempt"])
