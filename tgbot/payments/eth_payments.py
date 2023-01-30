from web3 import Web3

from tgbot.applecryptodb.apple_crypto_orm import DBCommands


async def check_eth_payment(item_price: int, tx_hash: str, web3: Web3, repo: DBCommands, config):
    tx_info = web3.eth.getTransaction(tx_hash)
    # recipient of ether
    recipient = tx_info["to"]
    # sender of ether
    sender = tx_info["from"]
    value = tx_info["value"]
    tx_hash_db = await repo.get_transaction_hash_eth(tx_hash)
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
