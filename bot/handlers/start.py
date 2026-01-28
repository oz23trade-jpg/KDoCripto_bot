from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from api.client import api_start
from texts import get_text, load_texts
from keyboards.inline import get_language_kb, get_main_menu

router = Router()

@router.message(CommandStart(deep_link=True))
async def cmd_start_ref(message: Message, regexp_command):
    ref_id = regexp_command.args  # start=ref_12345
    ref_id = int(ref_id.replace("ref_", "")) if ref_id.startswith("ref_") else None
    await cmd_start(message, referrer_id=ref_id)

@router.message(CommandStart())
async def cmd_start(message: Message, referrer_id: int | None = None):
    user = message.from_user
    profile = await api_start(user.id, user.username, user.full_name, referrer_id)
    
    if not profile:
        await message.answer("Error. Try later.")
        return

    lang = profile.get("lang", "en")
    load_texts(lang)

    if "returning" in profile:  # можно добавить флаг в API, или проверять joined_at
        text = get_text("welcome_returning", name=user.first_name or "")
    else:
        text = get_text("welcome_new")

    if not profile.get("lang_set", False):  # первый запуск
        await message.answer(text, reply_markup=get_language_kb())
    else:
        await message.answer(text, reply_markup=get_main_menu())