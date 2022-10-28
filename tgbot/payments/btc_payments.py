from bitcoinlib.wallets import Wallet
from bitcoinlib.services.services import Service

from tgbot.applecryptodb.apple_crypto_orm import DBCommands


async def check_btc_payment(address: str, price: int, repo: DBCommands):
    service = Service(network="testnet")
    key_balance = service.getbalance(address)
    key = await repo.get_key_from_db(address)
    if key:
        raise IndexError
    else:
        if key_balance >= price:
            return True
        else:
            return False


def generate_new_bitcoin_key(config):
    wallet = Wallet(config["payments"]["wallet_name"])
    new_key = wallet.new_key().address
    return new_key
