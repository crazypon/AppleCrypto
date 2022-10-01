import asyncio
import logging
import configparser
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher
from redis.asyncio.client import Redis
from tgbot.applecryptodb.sql import create_pool
from tgbot.middlewares.sesseionsender import DBMiddleware
from tgbot.handlers.user_handlers.show_categories import show_categories_router
from tgbot.handlers.user_handlers.navigator import navigator_router
from tgbot.handlers.admin_handlers.add_product import add_product_router
from tgbot.handlers.admin_handlers.get_product_name import get_product_name_router
from tgbot.handlers.admin_handlers.get_product_storage import get_product_storage_router
from tgbot.handlers.admin_handlers.get_product_color import get_product_color_router
from tgbot.handlers.admin_handlers.get_product_ram import get_product_ram_router
from tgbot.handlers.admin_handlers.get_product_category import get_product_category_router
from tgbot.handlers.admin_handlers.get_product_subcategory import get_product_subcategory_router
from tgbot.handlers.admin_handlers.get_product_gadget_name import get_product_gadget_name_router
from tgbot.handlers.admin_handlers.get_product_price import get_product_price_router
from tgbot.handlers.admin_handlers.get_product_photo import get_product_photo_router


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

    # user routers
    dp.include_router(show_categories_router)
    dp.include_router(navigator_router)
    # admin routers
    dp.include_router(add_product_router)
    dp.include_router(get_product_name_router)
    dp.include_router(get_product_storage_router)
    dp.include_router(get_product_color_router)
    dp.include_router(get_product_ram_router)
    dp.include_router(get_product_category_router)
    dp.include_router(get_product_subcategory_router)
    dp.include_router(get_product_gadget_name_router)
    dp.include_router(get_product_price_router)
    dp.include_router(get_product_photo_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        logger.info("Starting Bot")
    except KeyboardInterrupt:
        logger.info("Bot stopped")
