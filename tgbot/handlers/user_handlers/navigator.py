from aiogram import types
from tgbot.applecryptodb.apple_crypto_orm import DBCommands
from tgbot.handlers.user_handlers.resources import NavigationCD
from tgbot.handlers.user_handlers.show_categories import show_categories
from tgbot.handlers.user_handlers.show_subcategories import show_subcategories
from tgbot.handlers.user_handlers.show_gadget_names import show_gadget_names
from tgbot.handlers.user_handlers.show_all_items import show_all_items
from tgbot.handlers.router import user_router


@user_router.callback_query(NavigationCD.filter())
async def navigate(call: types.CallbackQuery, callback_data: NavigationCD, repo: DBCommands):
    level = callback_data.current_level
    handlers = {
        "1": show_categories,
        "2": show_subcategories,
        "3": show_gadget_names,
        "4": show_all_items
    }
    handler = handlers[str(level)]
    await handler(
        call,
        repo,
        category=callback_data.category,
        subcategory=callback_data.subcategory,
        gadget_name=callback_data.gadget_name
    )
