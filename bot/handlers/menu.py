# bot/handlers/menu.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from texts import get_text
import logging

router = Router()

logger = logging.getLogger(__name__)

# Mapping: callback_data → ключ текста из en.json
MENU_MAPPING = {
    "menu_learning": "learning_menu",
    "menu_earning": "earning_menu",
    "menu_referral": "referral_menu",
    "menu_quiz": "quiz_menu",
    "menu_lottery": "lottery_menu",
    "menu_support": "support_menu",
    "help": "help"
}


@router.callback_query(F.data.in_(MENU_MAPPING.keys()))
async def main_menus(cb: CallbackQuery):
    """Обработчик основных пунктов меню"""
    key = MENU_MAPPING.get(cb.data, "unknown_command")
    
    text = get_text(key)
    if not text:
        logger.warning(f"Text key not found: {key}")
        text = "Раздел в разработке. Вернись в главное меню."
    
    try:
        await cb.message.edit_text(
            text,
            reply_markup=cb.message.reply_markup  # сохраняем текущую клавиатуру
        )
    except Exception as e:
        logger.error(f"Error editing message: {e}")
        await cb.message.answer("Ошибка отображения меню. Попробуй снова.")
    
    await cb.answer()
