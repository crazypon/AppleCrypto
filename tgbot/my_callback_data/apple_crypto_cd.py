from aiogram.filters.callback_data import CallbackData


class NavigationCD(CallbackData, prefix="nav"):
    current_level: int
    category: str
    subcategory: str
    gadget_name: str
    item_id: int
