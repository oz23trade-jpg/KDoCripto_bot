from aiogram import Router
from aiogram.types import CallbackQuery
from api.client import api_set_language
from texts import load_texts, get_text
from keyboards.inline import get_main_menu

router = Router()

@router.callback_query(F.data.startswith("lang_"))
async def set_language(cb: CallbackQuery):
    lang = cb.data.split("_")[1]
    await api_set_language(cb.from_user.id, lang)
    load_texts(lang)
    
    await cb.message.edit_text(get_text("language_set"), reply_markup=get_main_menu())
    await cb.answer()