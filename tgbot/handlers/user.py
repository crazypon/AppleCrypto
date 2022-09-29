from typing import Union
from aiogram import F, Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.applecryptodb.apple_crypto_orm import DBCommands
from tgbot.my_callback_data.apple_crypto_cd import NavigationCD


router = Router()


async def categories_keyboard(repo: DBCommands):
    current_level = 1
    builder = InlineKeyboardBuilder()
    category_names = await repo.get_all_categories()
    for item in category_names:
        category_name = item[0]
        builder.button(text=f"{category_name}📱", callback_data=NavigationCD(
            current_level=current_level,
            category=category_name
        ))
    category_keyboard = builder.as_markup()
    return category_keyboard


async def subcategories_keyboard(category_name: str, repo: DBCommands):
    current_level = 2
    builder = InlineKeyboardBuilder()
    subcategories = await repo.get_all_subcategories(category_name)
    for item in subcategories:
        subcategory_name = item[0]
        builder.button(text=subcategory_name, callback_data=NavigationCD(
            current_level=current_level,
            subcategory=subcategory_name
        ))

    builder.button(text="⬅️ Back", callback_data=NavigationCD(current_level=current_level - 1))
    subcategories_kb = builder.as_markup()
    return subcategories_kb


async def gadget_names_keyboard(category_name: str, subcategory: str, repo: DBCommands):
    current_level = 3
    builder = InlineKeyboardBuilder()
    gadget_names = await repo.get_all_gadget_names(category_name, subcategory)
    for item in gadget_names:
        gadget_title = item[0]
        builder.button(text=gadget_title, callback_data=NavigationCD(
            current_level=current_level,
            category=category_name,
            subcategory=subcategory,
            gadget_name=gadget_title
        ))

    builder.button(text="⬅️ Back", callback_data=NavigationCD(
        current_level=current_level - 1,
        category=category_name,
        subcategory=subcategory
    ))


# TODO this code must be in handler
async def show_all_items(category_name: str, subcategory: str, gadget_name: str, repo: DBCommands):
    current_level = 4
    items = await repo.get_all_item_ids(category_name, subcategory, gadget_name)

    for item_id in items:
        builder = InlineKeyboardBuilder()
        builder.button(text="buy💵", callback_data=NavigationCD(
            current_level=current_level,
            category=category_name,
            subcategory=subcategory,
            gadget_name=gadget_name,
            item_id=item_id
        ))


async def show_categories(message: Union[types.Message, types.CallbackQuery], repo: DBCommands):
    await message.answer("Hello! choose what you want to buy", reply_markup=await categories_keyboard(repo))

