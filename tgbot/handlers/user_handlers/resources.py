from aiogram.filters.callback_data import CallbackData
from aiogram.filters.state import State, StatesGroup


class BuyItem(StatesGroup):
    check_payment = State()


class NavigationCD(CallbackData, prefix="nav"):
    current_level: int
    category: str
    subcategory: str
    gadget_name: str


class PaidCD(CallbackData, prefix="send"):
    item_price: int
    wallet_name: str
    address: str


class BuyCD(CallbackData, prefix="buy"):
    item_id: int


class MethodCD(CallbackData, prefix="method"):
    currency: str
    item_id: int


def make_callback_data(level, category="0", subcategory="0", gadget_name="0"):
    return NavigationCD(current_level=level, category=category, subcategory=subcategory, gadget_name=gadget_name)

