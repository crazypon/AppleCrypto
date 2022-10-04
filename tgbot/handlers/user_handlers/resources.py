from aiogram.filters.callback_data import CallbackData


class NavigationCD(CallbackData, prefix="nav"):
    current_level: int
    category: str
    subcategory: str
    gadget_name: str


class BuyCD(CallbackData, prefix="buy"):
    item_id: int


def make_callback_data(level, category="0", subcategory="0", gadget_name="0"):
    return NavigationCD(current_level=level, category=category, subcategory=subcategory, gadget_name=gadget_name)

