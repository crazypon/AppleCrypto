from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.applecryptodb.apple_crypto_orm import DBCommands
from tgbot.handlers.user_handlers.resources import make_callback_data


async def subcategories_keyboard(category: str, repo: DBCommands):
    current_level = 2
    builder = InlineKeyboardBuilder()
    subcategories = await repo.get_all_subcategories(category)
    amount_of_buttons = 1
    for item in set(subcategories):
        subcategory_name = item[0]
        builder.button(text=subcategory_name, callback_data=make_callback_data(level=current_level + 1,
                                                                               category=category,
                                                                               subcategory=subcategory_name))
        amount_of_buttons += 1

    builder.button(text="⬅️ Back",
                   callback_data=make_callback_data(level=current_level - 1, category=category))
    if amount_of_buttons % 2 == 1:
        builder.adjust(2)
    elif amount_of_buttons % 3 == 1:
        builder.adjust(3)
    subcategories_kb = builder.as_markup()
    return subcategories_kb


async def show_subcategories(call: types.CallbackQuery, repo: DBCommands, category, **kwargs):
    await call.message.edit_text("What you want to buy")
    await call.message.edit_reply_markup(await subcategories_keyboard(repo=repo, category=category))