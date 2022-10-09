import configparser
from datetime import datetime
import dateutil.parser as parser

from aiogram.filters.callback_data import CallbackData
from aiogram.filters.state import State, StatesGroup
import blockcypher as bc
import pyqrcode

from tgbot.handlers.user_handlers.create_invoice import Payment


class BuyItem(StatesGroup):
    check_payment = State()


class NavigationCD(CallbackData, prefix="nav"):
    current_level: int
    category: str
    subcategory: str
    gadget_name: str


class BuyCD(CallbackData, prefix="buy"):
    item_id: int


class PaidCD(CallbackData, prefix="check"):
    payment: Payment
    address: dict


def make_callback_data(level, category="0", subcategory="0", gadget_name="0"):
    return NavigationCD(current_level=level, category=category, subcategory=subcategory, gadget_name=gadget_name)


request_link = "bitcoin:{address}?" \
               "amount={amount}" \
               "&label={label}"


def make_qr_code(link):
    path = "/home/ilnur/PycharmProjects/AppleCrypto/qrcodes/qr_post_link.png"
    qr = pyqrcode.create(link, "L")
    qr.png(path, scale=6)
    return path


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


def check_payment(address: dict, amount: int, created: str):
    config = configparser.ConfigParser()
    config.read("bot.ini")
    # converting string iso to datetime iso
    created = parser.parse(created)

    details = bc.get_address_details(address=address, api_key=config["payments"]["blockcypher_token"])
    address_details = AddressDetails(**details)
    # checking not confirmed transactions
    for transaction in address_details.unconfirmed_txrefs:
        if transaction.get("value") == amount:
            if transaction.get("received") > created:
                if transaction.get("confirmations") > 0:
                    return True
                else:
                    raise NotConfirmed

    # Checking confirmed transactions
    for transaction in address_details.txrefs:
        if transaction.get("value") == amount:
            if transaction.get("received") > created:
                return True
    raise NoPaymentFound


# sending bitcoin to my main account
def send_to_myself(amount):
    config = configparser.ConfigParser()
    config.read("bot.ini")
    bc.simple_spend(
        from_privkey=config["payments"]["wallet_privkey"],
        to_address=config["payments"]["wallet_address"],
        api_key=config["payments"]["blockcypher_token"],
        to_satoshis=amount
    )
