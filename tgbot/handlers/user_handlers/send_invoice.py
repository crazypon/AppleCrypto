from aiogram import types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from blockcypher import from_base_unit

from tgbot.applecryptodb.apple_crypto_orm import DBCommands
from tgbot.handlers.router import user_router
from tgbot.handlers.user_handlers.resources import BuyCD
from tgbot.handlers.user_handlers.create_invoice import Payment


def paid_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Paid", callback_data="paid")
    kb = builder.as_markup()
    return kb


@user_router.callback_query(BuyCD.filter())
async def send_invoice(call: types.CallbackQuery, callback_data: BuyCD, repo: DBCommands):
    item_id = callback_data.item_id
    amount = await repo.get_item_price(item_id)
    payment = Payment(amount=amount)
    payment.create()

    # making function that converts satoshis in bitcoin
    show_amount = from_base_unit(amount, "btc")
    new_address = payment.generate_new_address()
    await call.message.answer(f"Pay {show_amount:8.f} btc, to\n"
                              f"{new_address }", reply_markup=paid_keyboard())


