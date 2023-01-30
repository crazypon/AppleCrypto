import asyncio
import logging
import configparser
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher
from bitcoinlib.wallets import Wallet, WalletError
from bitcoinlib.mnemonic import Mnemonic
from web3 import Web3
from redis.asyncio.client import Redis
from tgbot.applecryptodb.sql import create_pool
from tgbot.middlewares.sesseionsender import DBMiddleware
from tgbot.handlers.router import admin_router, user_router


logger = logging.getLogger(__name__)


async def main():
    config = configparser.ConfigParser()
    config.read("bot.ini")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
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
    # creating queue for reservations of ETH addresses
    queue = asyncio.Queue()

    # user routers
    dp.include_router(user_router)
    # admin routers
    dp.include_router(admin_router)

    # creating web3 instance
    web3 = Web3(Web3.HTTPProvider(config["payments"]["infura_url"]))

    # creating a wallet for btc
    try:
        pass_phrase = Mnemonic().generate()
        Wallet.create(config["payments"]["wallet_name"], keys=pass_phrase, network=config["payments"]["network"])
    except WalletError:
        pass
    else:
        print("---------- Warning! Write Down The Words Else You Will Not Have Access To Your Wallet! ----------------")
        print(pass_phrase)

    # sending web3 instance to every handler
    await dp.start_polling(bot, web3=web3, config=config)
    # starting scheduler for address reserve function

if __name__ == "__main__":
    try:
        asyncio.run(main())
        logger.info("Starting Bot")
    except KeyboardInterrupt:
        logger.info("Bot stopped")
