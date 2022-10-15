import configparser
from web3 import Web3
from eth_account import Account
import secrets


class NoEnoughMoney(Exception):
    pass


def send_ether_to_myself(address: str, amount: int):
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
        "value": amount,
        "gas": 2000000,
        "gasPrice": web3.toWei("50", "gwei")
    }

    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash


def check_eth_payment(address: str, item_price: int):
    config = configparser.ConfigParser()
    config.read("bot.ini")

    infura_url = config["payments"]["infura_url"]

    web3 = Web3(Web3.HTTPProvider(infura_url))
    balance = web3.eth.getBalance(address)
    if balance >= item_price:
        tx_hash = send_ether_to_myself(address, amount=item_price)
        return tx_hash
    else:
        raise NoEnoughMoney


def generate_new_eth_wallet():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    eth_address = acct.address
    return eth_address
