# bot/api/client.py
"""
Асинхронный HTTP-клиент для общения Telegram-бота с backend API.
"""

import aiohttp
import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
TIMEOUT = aiohttp.ClientTimeout(total=15)  # 15 секунд на весь запрос

# Глобальная сессия (создаётся один раз)
_session: Optional[aiohttp.ClientSession] = None

logger = logging.getLogger(__name__)


async def _get_session() -> aiohttp.ClientSession:
    """Возвращает общую сессию или создаёт новую"""
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession(timeout=TIMEOUT)
    return _session


async def _request(
    method: str,
    endpoint: str,
    params: Optional[Dict] = None,
    json: Optional[Dict] = None,
) -> Optional[Dict]:
    """Универсальный запрос к API с обработкой ошибок"""
    url = f"{API_BASE_URL}{endpoint}"
    
    session = await _get_session()
    
    try:
        async with session.request(
            method=method.upper(),
            url=url,
            params=params,
            json=json,
            headers={"Content-Type": "application/json"},
        ) as resp:
            if resp.status >= 400:
                error_text = await resp.text()
                logger.warning(f"API error {resp.status} at {url}: {error_text}")
                return None
            
            if resp.content_type.startswith("application/json"):
                return await resp.json()
            else:
                logger.warning(f"Unexpected content-type: {resp.content_type}")
                return None
                
    except aiohttp.ClientError as e:
        logger.error(f"API request failed: {e} → {url}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error in API request: {e}")
        return None


# ==================== Методы API ====================

async def api_start(
    user_id: int,
    username: Optional[str] = None,
    name: Optional[str] = None,
    referrer_id: Optional[int] = None,
) -> Optional[Dict]:
    """Регистрация / обновление пользователя при /start"""
    params = {
        "user_id": user_id,
        "username": username,
        "first_name": name,
        "referrer_id": referrer_id,
    }
    return await _request("POST", "/user/start", params=params)


async def api_set_language(user_id: int, lang: str) -> Optional[Dict]:
    """Смена языка пользователя"""
    json_data = {"user_id": user_id, "lang": lang}
    return await _request("POST", "/user/language", json=json_data)


async def api_get_profile(user_id: int) -> Optional[Dict]:
    """Получение профиля пользователя"""
    return await _request("GET", f"/user/{user_id}")


# ==================== Дополнительные полезные методы ====================

async def api_health_check() -> bool:
    """Проверка доступности backend"""
    result = await _request("GET", "/health")
    return bool(result and result.get("status") in ("ok", "healthy"))


# Закрытие сессии при завершении бота (можно вызвать в shutdown)
async def close_session():
    global _session
    if _session and not _session.closed:
        await _session.close()