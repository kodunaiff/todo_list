from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import Config
import asyncio

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! приступаем к разработке")

# Обработчик обычных сообщений
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Вы написали: {message.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())