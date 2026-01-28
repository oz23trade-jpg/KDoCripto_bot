# bot/keyboards/inline.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Константы для callback_data — чтобы не было опечаток
class CallbackData:
    MAIN_MENU = "main_menu"
    PROFILE = "profile"
    HELP = "help"
    MENU_LEARNING = "menu_learning"
    MENU_EARNING = "menu_earning"
    MENU_REFERRAL = "menu_referral"
    MENU_QUIZ = "menu_quiz"
    MENU_LOTTERY = "menu_lottery"
    MENU_SUPPORT = "menu_support"
    LANG_EN = "lang_en"
    LANG_RU = "lang_ru"
    LANG_FI = "lang_fi"


def get_main_menu() -> InlineKeyboardMarkup:
    """
    Главное меню бота — основная навигация.
    """
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
    """
    Клавиатура выбора языка при первом запуске.
    """
    kb = [
        [InlineKeyboardButton(text="🇬🇧 English", callback_data=CallbackData.LANG_EN)],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data=CallbackData.LANG_RU)],
        [InlineKeyboardButton(text="🇫🇮 Suomi", callback_data=CallbackData.LANG_FI)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)