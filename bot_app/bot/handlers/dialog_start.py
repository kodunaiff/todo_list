from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from bot.services.user_service import register_user


start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: Message):
    success = await register_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )

    if success:
        await message.answer("Привет! Ты успешно зарегистрирован(а)!")
    else:
        await message.answer("Привет! Не удалось завершить регистрацию. Попробуйте позже.")
