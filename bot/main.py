# bot/main.py

import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, __version__ as aiogram_version
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import settings

# ── Импорт роутеров ─────────────────────────────
from handlers.start import router as start_router
from handlers.language import router as lang_router
from handlers.profile import router as profile_router
from handlers.menu import router as menu_router
from handlers.referral import router as referral_router
from handlers.learning import router as learning_router
from handlers.quiz import router as quiz_router
from handlers.support import router as support_router


# ── Логирование ─────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)


# ── Инициализация бота ──────────────────────────
bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()


# ── Регистрация роутеров ────────────────────────
def register_routers():
    dp.include_router(start_router)
    dp.include_router(lang_router)
    dp.include_router(profile_router)
    dp.include_router(menu_router)
    dp.include_router(referral_router)
    dp.include_router(learning_router)
    dp.include_router(quiz_router)
    dp.include_router(support_router)


# ── События ─────────────────────────────────────
async def on_startup():
    logger.info(f"🚀 Бот запущен | aiogram v{aiogram_version}")


async def on_shutdown():
    logger.warning("⛔ Бот останавливается...")
    await bot.session.close()


# ── Запуск ──────────────────────────────────────
async def main():
    register_routers()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=settings.DROP_PENDING_UPDATES,
        )
    except Exception as e:
        logger.exception(f"Ошибка во время polling: {e}")
    finally:
        await on_shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен вручную")
