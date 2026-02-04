# bot/handlers/learning.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from texts import get_text
from keyboards.inline import get_main_menu, get_courses_kb, get_lesson_complete_kb
import logging

router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == "menu_learning")
async def show_learning_menu(cb: CallbackQuery):
    """Показывает меню выбора курсов"""
    text = get_text("learning_menu")
    if not text:
        text = "Раздел обучения временно недоступен."
    
    await cb.message.edit_text(text, reply_markup=get_courses_kb())
    await cb.answer()


@router.callback_query(F.data.startswith("start_course:"))
async def start_course(cb: CallbackQuery):
    """Начинает курс (пока статический пример)"""
    try:
        course_id = cb.data.split(":")[1]
    except IndexError:
        logger.error(f"Invalid course callback: {cb.data}")
        await cb.answer("Ошибка запуска курса", show_alert=True)
        return
    
    logger.info(f"Course started: user={cb.from_user.id}, course={course_id}")
    
    # Пока статический текст (в будущем — из API)
    text = (
        f"📖 Курс Crypto Basics (ID: {course_id})\n\n"
        "Уроки:\n"
        "1. Что такое Bitcoin? (незавершён)\n"
        "2. Как работают кошельки\n"
        "3. Основы безопасности\n\n"
        "Нажми на урок, чтобы начать."
    )
    
    # В будущем — клавиатура из API
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1. Что такое Bitcoin?", callback_data="open_lesson:1:1")],
        [InlineKeyboardButton(text="🔙 Назад к курсам", callback_data="menu_learning")]
    ])
    
    await cb.message.edit_text(text, reply_markup=kb)
    await cb.answer()


@router.callback_query(F.data.startswith("open_lesson:"))
async def open_lesson(cb: CallbackQuery):
    """Открывает конкретный урок"""
    try:
        _, course_id, lesson_id = cb.data.split(":")
        course_id, lesson_id = int(course_id), int(lesson_id)
    except (IndexError, ValueError):
        logger.error(f"Invalid lesson callback: {cb.data}")
        await cb.answer("Ошибка открытия урока", show_alert=True)
        return
    
    logger.info(f"Lesson opened: user={cb.from_user.id}, course={course_id}, lesson={lesson_id}")
    
    # Пока статический контент (в будущем — из API)
    text = (
        f"Урок {lesson_id} / Курс {course_id}\n\n"
        "Bitcoin — это первая и самая известная криптовалюта. "
        "Её создал человек или группа под псевдонимом Satoshi Nakamoto в 2008–2009 году.\n\n"
        "Основные идеи:\n"
        "- Децентрализация\n"
        "- Нет центрального банка\n"
        "- Ограниченная эмиссия (21 млн монет)"
    )
    
    kb = get_lesson_complete_kb(course_id=course_id, lesson_id=lesson_id)
    
    await cb.message.edit_text(text, reply_markup=kb)
    await cb.answer()


@router.callback_query(F.data.startswith("complete_lesson:"))
async def complete_lesson(cb: CallbackQuery):
    """Завершает урок и начисляет +5 points"""
    try:
        _, course_id, lesson_id = cb.data.split(":")
        course_id, lesson_id = int(course_id), int(lesson_id)
    except (IndexError, ValueError):
        logger.error(f"Invalid complete lesson callback: {cb.data}")
        await cb.answer("Ошибка завершения урока", show_alert=True)
        return
    
    user_id = cb.from_user.id
    logger.info(f"Lesson completed: user={user_id}, course={course_id}, lesson={lesson_id}")
    
    # Здесь должен быть реальный вызов API
    # await api_complete_lesson(user_id, lesson_id)
    
    text = (
        "✅ Урок завершён!\n\n"
        "+5 points добавлено на твой счёт\n"
        "Продолжай учиться и зарабатывать!"
    )
    
    await cb.message.edit_text(text, reply_markup=get_main_menu())
    await cb.answer("Урок засчитан! +5 points 🎉")
