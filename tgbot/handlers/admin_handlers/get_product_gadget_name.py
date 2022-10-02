from aiogram import types
from aiogram.fsm.context import FSMContext
from tgbot.handlers.admin_handlers.resources import AddProduct
from tgbot.handlers.router import admin_router


@admin_router.message(state=AddProduct.get_product_gadget_name)
async def get_product_gadget_name(message: types.Message, state: FSMContext):
    product_gadget_name = message.text
    await state.update_data(product_gadget_name=product_gadget_name)
    await message.answer("Enter product's price")
    await state.set_state(AddProduct.get_product_price)
