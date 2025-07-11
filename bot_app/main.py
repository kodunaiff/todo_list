# main.py

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram_dialog import setup_dialogs, DialogManager
from aiogram.filters import Command

from config import Config
from dialogs.add_task_dialog import add_task_dialog, AddTaskDialogSG

import asyncio

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Запускаем диалоги
dp.include_routers(add_task_dialog)
setup_dialogs(dp)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Используйте /add для создания новой задачи.")


@dp.message(Command("add"))
async def cmd_add(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AddTaskDialogSG.title)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())