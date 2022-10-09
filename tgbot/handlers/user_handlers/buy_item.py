import json

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
import blockcypher as bc

from tgbot.handlers.router import user_router
from tgbot.handlers.user_handlers.resources import BuyCD
from tgbot.handlers.user_handlers.create_invoice import Payment
from tgbot.applecryptodb.apple_crypto_orm import DBCommands
from tgbot.handlers.user_handlers.resources import request_link, make_qr_code, BuyItem, check_payment, NoPaymentFound
from tgbot.handlers.user_handlers.resources import NotConfirmed, send_to_myself


class PaymentSender(StatesGroup):
    btc = State()


def paid_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="paid", callback_data="paid")
    return builder.as_markup()


@user_router.callback_query(BuyCD.filter())
async def send_address(call: types.CallbackQuery, callback_data: BuyCD, repo: DBCommands, state: FSMContext):
    item_id = callback_data.item_id
    price = await repo.get_item_price(item_id=item_id)

    payment = Payment(amount=price)
    payment.create()
    # this is brand-new address
    new_address = payment.generate_new_address()
    show_amount = bc.from_base_unit(price, "btc")
    qr_link = request_link.format(address=new_address, amount=price, label="test")
    qr_code = make_qr_code(qr_link)
    await call.message.answer(f"Send {show_amount} btc to the\n"
                              f"<code>{new_address}</code> address", parse_mode="HTML",
                              reply_markup=paid_keyboard())
    await call.message.answer_photo(types.FSInputFile(qr_code))

    await state.update_data(payment=payment.to_json())
    await state.update_data(address=new_address)
    await state.set_state(BuyItem.check_payment)


@user_router.callback_query()
async def check_address(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payment_string = data["payment"]
    payment = json.loads(payment_string)
    address = data["address"]
    try:
        check_payment(address=address, amount=payment["amount"], created=payment["created"])
    except NotConfirmed:
        await call.message.answer("Transaction has found but not approved, please try later")
        return
    except NoPaymentFound:
        await call.message.answer("Transaction has not found")
        return
    else:
        await call.message.answer("Payment successfully approved!")
        send_to_myself(payment["amount"])


