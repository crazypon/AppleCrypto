from typing import Union
from aiogram import types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.applecryptodb.apple_crypto_orm import DBCommands
from tgbot.handlers.user_handlers.resources import make_callback_data, user_router


async def categories_keyboard(repo: DBCommands):
    current_level = 1
    builder = InlineKeyboardBuilder()
    category_names = await repo.get_all_categories()
    amount_of_buttons = 0
    for item in set(category_names):
        category_name = item[0]
        builder.button(text=f"{category_name} 🍏", callback_data=make_callback_data(level=current_level + 1,
                                                                                  category=category_name))
        amount_of_buttons += 1
    if amount_of_buttons % 2 == 1:
        builder.adjust(2)
    elif amount_of_buttons % 3 == 1:
        builder.adjust(3)
    category_keyboard = builder.as_markup()
    return category_keyboard


@user_router.message(commands=["buy"])
async def show_categories(message: Union[types.Message, types.CallbackQuery], repo: DBCommands, **kwargs):
    if isinstance(message, types.Message):
        await message.answer("Hello! choose what you want to buy", reply_markup=await categories_keyboard(repo))
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_reply_markup(await categories_keyboard(repo))
