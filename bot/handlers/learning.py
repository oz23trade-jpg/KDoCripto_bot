# bot/handlers/learning.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from texts import get_text
from keyboards.inline import get_main_menu, get_courses_kb, get_lesson_complete_kb

router = Router()


@router.callback_query(F.data == "menu_learning")
async def show_learning_menu(cb: CallbackQuery):
    """Показывает меню выбора курсов"""
    text = get_text("learning_menu")
    await cb.message.edit_text(text, reply_markup=get_courses_kb())
    await cb.answer()


@router.callback_query(F.data.startswith("start_course:"))
async def start_course(cb: CallbackQuery):
    """Начинает курс (пока только один курс — можно расширять)"""
    course_id = cb.data.split(":")[1]  # например "start_course:1" → "1"
    
    # Пока просто текст + список уроков (в будущем — динамика из БД)
    text = (
        f"📖 Курс Crypto Basics (ID: {course_id})\n\n"
        "Уроки:\n"
        "1. Что такое Bitcoin? (незавершён)\n"
        "2. Как работают кошельки\n"
        "3. Основы безопасности\n\n"
        "Нажми на урок, чтобы начать."
    )
    
    # В будущем здесь будет клавиатура с уроками из БД
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1. Что такое Bitcoin?", callback_data="open_lesson:1:1")],
        [InlineKeyboardButton(text="🔙 Назад к курсам", callback_data="menu_learning")]
    ])
    
    await cb.message.edit_text(text, reply_markup=kb)
    await cb.answer()


@router.callback_query(F.data.startswith("open_lesson:"))
async def open_lesson(cb: CallbackQuery):
    """Открывает конкретный урок"""
    _, course_id, lesson_id = cb.data.split(":")  # "open_lesson:1:1" → course=1, lesson=1
    
    # Пока статический контент (в будущем — из БД)
    text = (
        f"Урок {lesson_id} / Курс {course_id}\n\n"
        "Bitcoin — это первая и самая известная криптовалюта. "
        "Её создал человек или группа под псевдонимом Satoshi Nakamoto в 2008–2009 году.\n\n"
        "Основные идеи:\n"
        "- Децентрализация\n"
        "- Нет центрального банка\n"
        "- Ограниченная эмиссия (21 млн монет)"
    )
    
    kb = get_lesson_complete_kb(course_id=int(course_id), lesson_id=int(lesson_id))
    
    await cb.message.edit_text(text, reply_markup=kb)
    await cb.answer()


@router.callback_query(F.data.startswith("complete_lesson:"))
async def complete_lesson(cb: CallbackQuery):
    """Завершает урок и начисляет +5 points"""
    _, course_id, lesson_id = cb.data.split(":")  # "complete_lesson:1:1"
    
    user_id = cb.from_user.id
    
    # Здесь должен быть вызов API backend'а для начисления points
    # Пока просто имитация
    text = (
        "✅ Урок завершён!\n\n"
        "+5 points добавлено на твой счёт\n"
        "Продолжай учиться и зарабатывать!"
    )
    
    await cb.message.edit_text(text, reply_markup=get_main_menu())
    await cb.answer("Урок засчитан! +5 points 🎉")
