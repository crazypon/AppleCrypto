import configparser
from decimal import Decimal

import pyqrcode
from typing import Union
from bitcoinlib.wallets import Wallet
from web3 import Web3
from eth_account import Account
import secrets


request_link = "bitcoin:{address}?" \
               "amount={amount}" \
               "&label={label}"


class NoEnoughMoney(Exception):
    pass


def make_qr_code(link):
    path = "/home/ilnur/PycharmProjects/AppleCrypto/qrcodes/qr_post_link.png"
    qr = pyqrcode.create(link, "L")
    qr.png(path, scale=6)
    return path


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


def send_ether_to_myself(address):
    config = configparser.ConfigParser()
    config.read("bot.ini")
    infura_url = config["payments"]["infura_url"]
    private_key = config["payments"]["ether_priv_key"]
    main_eth_wallet = config["payments"]["wallet_address_eth"]

    web3 = Web3(Web3.HTTPProvider(infura_url))

    nonce = web3.eth.getTransactionCount(address)

    tx = {
        "nonce": nonce,
        "to": main_eth_wallet,
        "value": web3.toWei(0.001, "ether"),
        "gas": 2000000,
        "gasPrice": web3.toWei("50", "gwei")
    }

    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(tx_hash)


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


def generate_new_eth_wallet():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    eth_address = acct.address
    return eth_address
