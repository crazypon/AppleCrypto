from aiogram.filters.callback_data import CallbackData


class NavigationCD(CallbackData, prefix="nav"):
    current_level: int
    category: str
    subcategory: str
    gadget_name: str


class BuyCD(CallbackData, prefix="buy"):
    item_id: int
