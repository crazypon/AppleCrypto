from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest
from tgbot.applecryptodb.apple_crypto_orm import DBCommands
from tgbot.handlers.user_handlers.resources import make_callback_data


async def gadget_names_keyboard(category: str, subcategory: str, repo: DBCommands):
    current_level = 3
    builder = InlineKeyboardBuilder()
    gadget_names = await repo.get_all_gadget_names(category, subcategory)
    amount_of_buttons = 1
    for item in set(gadget_names):
        gadget_title = item[0]
        builder.button(text=gadget_title, callback_data=make_callback_data(level=current_level + 1,
                                                                           category=category,
                                                                           subcategory=subcategory,
                                                                           gadget_name=gadget_title))
        amount_of_buttons += 1
    builder.button(text="⬅️ Back", callback_data=make_callback_data(
        level=current_level - 1,
        category=category,
        subcategory=subcategory
    ))
    if amount_of_buttons % 2 == 1:
        builder.adjust(2)
    elif amount_of_buttons % 3 == 1:
        builder.adjust(3)
    return builder.as_markup()


async def show_gadget_names(call: types.CallbackQuery, repo: DBCommands, category, subcategory, **kwargs):
    try:
        await call.message.edit_text("Which generation you want to buy?")
        await call.message.edit_reply_markup(await gadget_names_keyboard(category=category,
                                                                         subcategory=subcategory,
                                                                         repo=repo))
    except TelegramBadRequest:
        await call.message.answer("Which generation you want to buy?",
                                  reply_markup=await gadget_names_keyboard(category=category,
                                                                           subcategory=subcategory,
                                                                           repo=repo))
