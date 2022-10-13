from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.handlers.router import user_router
from tgbot.handlers.user_handlers.resources import BuyCD, MethodCD


def make_methods_keyboard(item_id: int):
    methods_builder = InlineKeyboardBuilder()
    methods_builder.button(text="Bitcoin", callback_data=MethodCD(currency="bitcoin", item_id=item_id))
    methods_builder.button(text="Ethereum", callback_data=MethodCD(currency="ethereum", item_id=item_id))
    return methods_builder.as_markup()


@user_router.callback_query(BuyCD.filter())
async def send_payment_method(call: types.CallbackQuery, callback_data: BuyCD):
    item_id = callback_data.item_id
    await call.message.answer("Choose payment method", reply_markup=make_methods_keyboard(item_id))
