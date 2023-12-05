import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from handlers import start_handler, make_post_handler
from settings import settings

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    bot = Bot(settings.TOKEN.get_secret_value(), parse_mode=ParseMode.MARKDOWN_V2)
    dp = Dispatcher()

    dp.include_routers(
        start_handler.router,
        make_post_handler.router
    )
    await bot.delete_webhook()
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
