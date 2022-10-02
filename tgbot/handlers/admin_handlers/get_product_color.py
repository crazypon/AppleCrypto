from aiogram import types
from aiogram.fsm.context import FSMContext
from tgbot.handlers.admin_handlers.resources import AddProduct
from tgbot.handlers.router import admin_router


@admin_router.message(state=AddProduct.get_product_color)
async def get_product_color(message: types.Message, state: FSMContext):
    product_color = message.text
    await state.update_data(product_color=product_color)
    await message.answer("Enter product's ram amount")
    await state.set_state(AddProduct.get_product_ram)