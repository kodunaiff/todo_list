import aiohttp
import logging

BACKEND_URL = "http://backend:8000/api/users/"
logger = logging.getLogger(__name__)


async def register_user(telegram_id: int, username: str = None) -> bool:
    """Отправляет данные пользователя на backend"""
    user_data = {
        "telegram_id": telegram_id,
        "username": username
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                BACKEND_URL,
                json=user_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status in (200, 201):
                    return True
                else:
                    error = await response.text()
                    logger.error(f"Ошибка регистрации: {error}")
                    return False
    except Exception as e:
        logger.error(f"Ошибка при регистрации пользователя: {e}")
        return False
