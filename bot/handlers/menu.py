# bot/handlers/menu.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from texts import get_text
import logging

router = Router()

logger = logging.getLogger(__name__)

# Mapping: callback_data → ключ текста из en.json (или ru/fi)
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
    user_id = cb.from_user.id
    callback_data = cb.data
    logger.debug(f"Menu callback: user={user_id}, data={callback_data}")

    key = MENU_MAPPING.get(callback_data, "unknown_command")
    
    text = get_text(key)
    if not text:
        logger.warning(f"Text key not found: {key} for user {user_id}")
        text = "Этот раздел пока в разработке. Вернись в главное меню."

    try:
        await cb.message.edit_text(
            text,
            reply_markup=cb.message.reply_markup  # сохраняем текущую клавиатуру
        )
    except Exception as e:
        logger.error(f"Error editing message for user {user_id}: {e}")
        try:
            await cb.message.answer(text, reply_markup=cb.message.reply_markup)
        except Exception as e2:
            logger.error(f"Fallback answer failed for user {user_id}: {e2}")
            await cb.answer("Ошибка отображения меню", show_alert=True)
    
    await cb.answer()
