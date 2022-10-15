import configparser
from typing import Union
from bitcoinlib.wallets import Wallet


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


def check_btc_payment(wallet: Wallet, item_price: Union[float, int]):
    # amount of cryptocurrency that was sent by user to the "trial" address
    balance = wallet.balance_update_from_serviceprovider(network="testnet")
    if item_price <= balance:
        transaction_hash = send_btc_to_myself(wallet)
        return transaction_hash
    elif 0 < balance < item_price:
        raise NoEnoughMoney
    else:
        return False


def generate_new_btc_wallet(user_id: int, wallet_id: Union[float, int]):
    config = configparser.ConfigParser()
    config.read("bot.ini")
    wallet_name = f"{str(user_id)}_{str(wallet_id)}"
    next_wallet_id = wallet_id + 1
    wallet = Wallet.create(wallet_name, network=config["payments"]["network"])
    result = {"wallet_name": wallet_name, "wallet": wallet, "next_wallet_id": next_wallet_id}
    return result
