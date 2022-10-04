import configparser
from dataclasses import dataclass
from datetime import datetime

from dateutil.tz import tzutc
import blockcypher as bc


class AddressDetails:
    def __init__(self,
                 address: dict,
                 total_received: int,
                 total_sent: int,
                 balance: int,
                 unconfirmed_balance: int,
                 unconfirmed_txrefs: list,
                 txrefs: list,
                 **kwargs):
        self.address = address
        self.total_received = total_received
        self.total_sent = total_sent
        self.balance = balance
        self.unconfirmed_balance = unconfirmed_balance
        self.unconfirmed_txrefs = unconfirmed_txrefs
        self.txrefs = txrefs


class NotConfirmed(Exception):
    pass


class NoPaymentFound(Exception):
    pass


@dataclass
class Payment:
    amount: int
    created: datetime
    success: bool

    def create(self):
        self.created = datetime.now(tz=tzutc())

    def check_payment(self, address):
        config = configparser.ConfigParser()
        config.read("bot.ini")
        details = bc.get_address_details(address=address, api_key=config["payments"]["blockcypher_token"])
        address_details = AddressDetails(**details)
        # checking not confirmed transactions
        for transaction in address_details.unconfirmed_txrefs:
            if transaction.get("value") == self.amount:
                if transaction.get("received") > self.created:
                    if transaction.get("confirmations") > 0:
                        return True
                    else:
                        raise NotConfirmed

        # Checking confirmed transactions
        for transaction in address_details.txrefs:
            if transaction.get("value") == self.amount:
                if transaction.get("received") > self.created:
                    return True
        raise NoPaymentFound

    # generating new address for accepting bitcoin
    def generate_new_address(self):
        config = configparser.ConfigParser()
        config.read("bot.ini")
        address = bc.generate_new_address(api_key=config["payments"]["blockcypher_token"])
        return address



