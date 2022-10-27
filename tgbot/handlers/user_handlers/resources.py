from aiogram.filters.callback_data import CallbackData
from aiogram.filters.state import State, StatesGroup
from pycoingecko.api import CoinGeckoAPI


class BuyItem(StatesGroup):
    check_payment = State()


class NavigationCD(CallbackData, prefix="nav"):
    current_level: int
    category: str
    subcategory: str
    gadget_name: str


class PaidCD(CallbackData, prefix="send"):
    item_price: int
    currency: str
    address: str


class BuyCD(CallbackData, prefix="buy"):
    item_id: int


class MethodCD(CallbackData, prefix="method"):
    currency: str
    item_id: int


def make_callback_data(level, category="0", subcategory="0", gadget_name="0"):
    return NavigationCD(current_level=level, category=category, subcategory=subcategory, gadget_name=gadget_name)


def convert_to_crypto(cg: CoinGeckoAPI, price: int, currency: str):
    # converting dollars to crypto in the smallest currency like satoshi or wei
    raw_crypto_price = cg.get_price(ids=currency, vs_currencies="usd")  # getting price of crypto
    crypto_price = raw_crypto_price[currency]["usd"]
    raw_item_price = price / crypto_price
    item_price = round(raw_item_price, 8)
    number = 10 ** 8
    smallest_price = item_price * number
    return smallest_price

