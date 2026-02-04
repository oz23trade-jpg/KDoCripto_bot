# bot/handlers/start.py
import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from api.client import api_start
from texts import get_text, load_texts
from keyboards.inline import get_language_kb, get_main_menu

router = Router()

logger = logging.getLogger(__name__)


@router.message(CommandStart(deep_link=True))
async def cmd_start_ref(message: Message, regexp_command):
    """Обработка /start с реферальной ссылкой (deep link)"""
    args = regexp_command.args
    referrer_id = None
    
    if args and args.startswith("ref_"):
        try:
            referrer_id = int(args.replace("ref_", ""))
            logger.info(f"Referral start detected: user={message.from_user.id}, referrer={referrer_id}")
        except ValueError:
            logger.warning(f"Invalid ref_id in deep link: {args}")
    
    await cmd_start(message, referrer_id=referrer_id)


@router.message(CommandStart())
async def cmd_start(message: Message, referrer_id: Optional[int] = None):
    """Основной обработчик /start"""
    user = message.from_user
    logger.info(f"Start command: user={user.id}, referrer={referrer_id}")

    try:
        profile = await api_start(
            user_id=user.id,
            username=user.username,
            name=user.full_name,
            referrer_id=referrer_id
        )
        
        if not profile:
            await message.answer("Ошибка сервера. Попробуй позже.")
            return

        lang = profile.get("lang", "en")
        load_texts(lang)

        if profile.get("is_new", True):  # Лучше использовать реальный флаг из API
            text = get_text("welcome_new")
        else:
            text = get_text("welcome_returning", name=user.first_name or "")

        if profile.get("lang_set", False):
            await message.answer(text, reply_markup=get_main_menu())
        else:
            await message.answer(text, reply_markup=get_language_kb())

    except Exception as e:
        logger.exception(f"Error in /start handler: {e}")
        await message.answer("Произошла ошибка. Попробуй позже.")
