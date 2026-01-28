from aiogram import Router
from aiogram.types import CallbackQuery
from texts import get_text

router = Router()

@router.callback_query(F.data.in_({"menu_learning", "menu_earning", "menu_referral", "menu_quiz", "menu_lottery", "menu_support", "help"}))
async def main_menus(cb: CallbackQuery):
    mapping = {
        "menu_learning": "learning_menu",
        "menu_earning": "earning_menu",
        "menu_referral": "referral_menu",
        "menu_quiz": "quiz_menu",
        "menu_lottery": "lottery_menu",
        "menu_support": "support_menu",
        "help": "help"
    }
    key = mapping.get(cb.data, "unknown_command")
    text = get_text(key)
    await cb.message.edit_text(text, reply_markup=cb.message.reply_markup)
    await cb.answer()