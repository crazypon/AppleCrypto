import configparser
from web3 import Web3
from web3.auto import w3
from eth_account import Account
import secrets
from tgbot.applecryptodb.apple_crypto_orm import DBCommands



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
        "value": web3.toWei(1, "ether"),
        "gas": 2000000,
        "gasPrice": web3.toWei("50", "gwei")
    }

    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash


async def check_eth_payment(item_price: int, tx_hash: str, web3: Web3, repo: DBCommands, config):
    tx_info = web3.eth.getTransaction(tx_hash)
    # recipient of ether
    recipient = tx_info["to"]
    value = tx_info["value"]
    tx_hash_db = await repo.get_transaction_hash(tx_hash)
    if not tx_hash_db:
        if recipient == config["payments"]["wallet_address_eth"]:
            if value >= item_price:
                return True
            else:
                raise ValueError("No enough money sent!")
        else:
            raise IndexError("Wrong address tx_hash")
    else:
        raise EOFError("This tx_hash is from your previous purchase")


def generate_new_eth_wallet():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    eth_address = acct.address
    return eth_address
