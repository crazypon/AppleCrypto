import asyncio
import logging
import configparser
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher
from redis.asyncio.client import Redis

from tgbot.applecryptodb.sql import create_pool
from tgbot.handlers.user_handlers.resources import user_router
from tgbot.handlers.admin_handlers.admin import admin_router
from tgbot.middlewares.sesseionsender import DBMiddleware

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
    dp.update.middleware(DBMiddleware(await create_pool(
        user=config["db"]["user"],
        password=config["db"]["password"],
        host=config["db"]["host"],
        database=config["db"]["database"]
    )))

    # my routers
    dp.include_router(user_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        logger.info("Starting Bot")
    except KeyboardInterrupt:
        logger.info("Bot stopped")
