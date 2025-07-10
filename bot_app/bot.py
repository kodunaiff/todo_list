from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import Config
import asyncio
import aiohttp
import json


bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()

BACKEND_URL = "http://backend:8000/api/users/"


async def register_user(telegram_id: int, username: str = None) -> bool:
    """Отправляет данные пользователя на бэкенд для регистрации"""
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
                if response.status == 201:
                    return True
                # Если пользователь уже существует (статус 200)
                elif response.status == 200:
                    return True
                else:
                    print(f"Ошибка регистрации: {await response.text()}")
                    return False
    except Exception as e:
        print(f"Ошибка при отправке запроса: {e}")
        return False

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Регистрируем пользователя
    success = await register_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )

    if success:
        await message.answer("Привет! Ты успешно зарегистрирован(а)!")
    else:
        await message.answer("Привет! Не удалось завершить регистрацию. Попробуйте позже.")


# Обработчик обычных сообщений
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Вы написали: {message.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())