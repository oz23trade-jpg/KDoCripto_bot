# bot/handlers/language.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from api.client import api_set_language
from texts import load_texts, get_text
from keyboards.inline import get_main_menu
import logging

router = Router()

logger = logging.getLogger(__name__)

VALID_LANGS = {"en", "ru", "fi"}


@router.callback_query(F.data.startswith("lang_"))
async def set_language(cb: CallbackQuery):
    try:
        lang = cb.data.split("_")[1].strip().lower()
        
        if lang not in VALID_LANGS:
            logger.warning(f"Invalid language callback: {cb.data} from user {cb.from_user.id}")
            await cb.answer("Неверный язык", show_alert=True)
            return

        # Сохраняем язык в backend
        response = await api_set_language(cb.from_user.id, lang)
        if not response:
            logger.error(f"API set_language failed for user {cb.from_user.id}")
            await cb.answer("Ошибка сервера. Попробуй позже", show_alert=True)
            return

        # Обновляем локальные тексты
        load_texts(lang)
        
        # Обновляем сообщение
        await cb.message.edit_text(
            get_text("language_set"),
            reply_markup=get_main_menu()
        )
        
        logger.info(f"Language changed to {lang} for user {cb.from_user.id}")
        await cb.answer(f"Язык изменён на {lang.upper()}")

    except IndexError:
        logger.error(f"Invalid callback data format: {cb.data}")
        await cb.answer("Ошибка обработки. Попробуй снова", show_alert=True)
    except Exception as e:
        logger.exception(f"Error in set_language handler: {e}")
        await cb.answer("Произошла ошибка. Попробуй позже", show_alert=True)
