import configparser
from typing import Union

from bitcoinlib.wallets import Wallet
from bitcoinlib.services.services import Service

from tgbot.applecryptodb.apple_crypto_orm import DBCommands


class NoEnoughMoney(Exception):
    pass


# sending bitcoin to my main account
def send_btc_to_myself(wallet: Wallet):
    config = configparser.ConfigParser()
    config.read("bot.ini")
    wallet.transactions_update()
    wallet_info = wallet.as_dict()
    main_wallet = config["payments"]["wallet_address_btc"]
    # getting all balance in str
    amount_str = wallet_info["main_balance_str"]
    # converting btc string into satoshis
    amount, _ = amount_str.split(" ")
    num = 10 ** 8
    price_in_satoshis = float(amount) * num
    tx_fee = 1024
    total_price = int(price_in_satoshis) - tx_fee
    wallet.utxos_update(networks="testnet")
    wallet.get_keys()
    wallet.scan()
    wallet.transactions_update()
    wallet.transactions_update_confirmations()
    transaction_hash = wallet.send_to(main_wallet, amount=total_price, fee=tx_fee, offline=False)
    transaction_hash.update_totals()

    return transaction_hash


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
