from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.applecryptodb.apple_crypto_orm import DBCommands
from tgbot.handlers.user_handlers.resources import make_callback_data, BuyCD


async def show_all_items(call: types.CallbackQuery, repo: DBCommands, category: str, subcategory: str,
                         gadget_name: str):
    await call.message.answer("Here are our searching results!")
    current_level = 4
    items = await repo.get_all_items(category, subcategory, gadget_name)
    for item in items:
        message_format = f"Model: {item[1]}\n" \
                         f"Price: ${item[2]}\n" \
                         f"\n" \
                         f"Storage: {item[3]} GB\n" \
                         f"Ram: {item[4]} GB\n" \
                         f"Color: {item[5]}"
        builder = InlineKeyboardBuilder()
        builder.button(text="Buy💸", callback_data=BuyCD(item_id=int(item[0])))
        builder.button(text="⬅️ Back", callback_data=make_callback_data(
            level=current_level - 1,
            category=category,
            subcategory=subcategory,
            gadget_name=gadget_name
        ))
        item_keyboard = builder.as_markup()
        await call.message.answer_photo(photo=item[6], caption=message_format, reply_markup=item_keyboard)


