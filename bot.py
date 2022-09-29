import asyncio
import logging
import configparser
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher, types
from redis.client import Redis
from tgbot.handlers import user
from tgbot.handlers.admin import admin_router

logger = logging.getLogger(__name__)


async def main():
    config = configparser.ConfigParser()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    config.read("bot.ini")
    bot = Bot(token=config["tgbot"]["token"])
    my_redis = Redis(
        host="localhost",
        port=6379
    )
    storage = RedisStorage(redis=my_redis)
    dp = Dispatcher(storage=storage)

    # my routers
    dp.include_router(user.router)
    dp.include_router(admin_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        logger.info("Starting Bot")
    except KeyboardInterrupt:
        logger.info("Bot stopped")
