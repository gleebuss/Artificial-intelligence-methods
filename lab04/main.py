"""Модуль запускает бота и начинает опрос, обрабатывая ответы пользователей."""
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bot.handlers import router
from dotenv import load_dotenv


async def main():
    """Основная асинхронная функция для запуска бота."""
    load_dotenv()
    bot = Bot(token=os.getenv('API_TOKEN'))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    commands = [
        BotCommand(command="/start", description="Начало опроса"),
        BotCommand(command="/model", description="Выбор модели"),
    ]
    await bot.set_my_commands(commands=commands)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())