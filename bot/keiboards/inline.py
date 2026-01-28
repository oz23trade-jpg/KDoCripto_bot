# bot/keyboards/inline.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Константы callback_data (защита от опечаток)
class CallbackData:
    MAIN_MENU       = "main_menu"
    PROFILE         = "profile"
    HELP            = "help"
    MENU_LEARNING   = "menu_learning"
    MENU_EARNING    = "menu_earning"
    MENU_REFERRAL   = "menu_referral"
    MENU_QUIZ       = "menu_quiz"
    MENU_LOTTERY    = "menu_lottery"
    MENU_SUPPORT    = "menu_support"

    LANG_EN         = "lang_en"
    LANG_RU         = "lang_ru"
    LANG_FI         = "lang_fi"

    REF_COPY        = "ref_copy"
    SUPPORT_SMALL   = "support_buy:small"
    SUPPORT_MEDIUM  = "support_buy:medium"
    SUPPORT_LARGE   = "support_buy:large"

    # Для уроков и квизов (примеры)
    START_COURSE    = "start_course:"
    OPEN_LESSON     = "open_lesson:"
    COMPLETE_LESSON = "complete_lesson:"
    QUIZ_ANSWER     = "quiz_ans:"


def get_main_menu() -> InlineKeyboardMarkup:
    """Главное меню бота"""
    kb = [
        [InlineKeyboardButton(text="📚 Learning", callback_data=CallbackData.MENU_LEARNING)],
        [InlineKeyboardButton(text="💰 Earn More", callback_data=CallbackData.MENU_EARNING)],
        [InlineKeyboardButton(text="👥 Referrals", callback_data=CallbackData.MENU_REFERRAL)],
        [InlineKeyboardButton(text="🧠 Quiz", callback_data=CallbackData.MENU_QUIZ)],
        [InlineKeyboardButton(text="🎰 Lottery", callback_data=CallbackData.MENU_LOTTERY)],
        [InlineKeyboardButton(text="❤️ Support", callback_data=CallbackData.MENU_SUPPORT)],
        [
            InlineKeyboardButton(text="👤 Profile", callback_data=CallbackData.PROFILE),
            InlineKeyboardButton(text="❓ Help", callback_data=CallbackData.HELP)
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_language_kb() -> InlineKeyboardMarkup:
    """Выбор языка при первом запуске"""
    kb = [
        [InlineKeyboardButton(text="🇬🇧 English", callback_data=CallbackData.LANG_EN)],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data=CallbackData.LANG_RU)],
        [InlineKeyboardButton(text="🇫🇮 Suomi", callback_data=CallbackData.LANG_FI)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_referral_menu_kb(user_id: int, bot_username: str) -> InlineKeyboardMarkup:
    """Клавиатура реферального меню"""
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    
    kb = [
        [
            InlineKeyboardButton(
                text="📤 Поделиться ссылкой",
                switch_inline_query_current_chat=(
                    f"Присоединяйся к K DoCripto! Учи крипту, зарабатывай очки и билеты 🚀\n"
                    f"Ссылка: {ref_link}"
                )
            )
        ],
        [InlineKeyboardButton(text="📋 Скопировать ссылку", callback_data=CallbackData.REF_COPY)],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data=CallbackData.MAIN_MENU)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_support_tiers_kb() -> InlineKeyboardMarkup:
    """Клавиатура уровней поддержки (Telegram Stars)"""
    kb = [
        [InlineKeyboardButton(text="☕ Small (100 Stars) → 5 tickets", callback_data=CallbackData.SUPPORT_SMALL)],
        [InlineKeyboardButton(text="🔥 Medium (500 Stars) → 30 tickets + badge", callback_data=CallbackData.SUPPORT_MEDIUM)],
        [InlineKeyboardButton(text="🚀 Large (1000 Stars) → 100 tickets + exclusive badge", callback_data=CallbackData.SUPPORT_LARGE)],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data=CallbackData.MAIN_MENU)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_courses_kb() -> InlineKeyboardMarkup:
    """Клавиатура выбора курсов (пока один курс — можно расширять)"""
    kb = [
        [InlineKeyboardButton(text="📖 Crypto Basics (Course 1)", callback_data=f"{CallbackData.START_COURSE}1")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data=CallbackData.MAIN_MENU)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_lesson_complete_kb(course_id: int, lesson_id: int) -> InlineKeyboardMarkup:
    """Кнопка завершения урока"""
    kb = [
        [InlineKeyboardButton(
            text="✅ Завершить урок (+5 points)",
            callback_data=f"{CallbackData.COMPLETE_LESSON}{course_id}:{lesson_id}"
        )],
        [InlineKeyboardButton(text="🔙 Назад к урокам", callback_data=CallbackData.MENU_LEARNING)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_quiz_options_kb(quiz_id: int, question_idx: int, options: list[str]) -> InlineKeyboardMarkup:
    """
    Динамическая клавиатура для вариантов ответа в квизе.
    Пример вызова: get_quiz_options_kb(1, 0, ["A. Bitcoin", "B. Ethereum", "C. Dogecoin"])
    """
    kb = []
    for idx, option in enumerate(options):
        kb.append([
            InlineKeyboardButton(
                text=option,
                callback_data=f"{CallbackData.QUIZ_ANSWER}{quiz_id}:{question_idx}:{idx}"
            )
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=kb)Markup(inline_keyboard=kb)
