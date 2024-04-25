import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from settings import TOKEN
from app.handlers import router

bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(router)


async def main() -> None:
    # add menu with commands
    await bot.set_my_commands(commands=[
        types.BotCommand(command="/start", description="Старт бот"),
        types.BotCommand(command="/menu", description="Main menu"),
        types.BotCommand(command="/films", description="Фільми"),
        types.BotCommand(command="/create_film", description="Додати новий фільм"),
        types.BotCommand(command="/cancel", description="Відміна додавання фільму"),
    ]
    )
    # Почнемо обробляти події для бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
