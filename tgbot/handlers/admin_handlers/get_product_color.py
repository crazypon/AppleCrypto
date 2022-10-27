from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from tgbot.handlers.admin_handlers.resources import AddProduct
from tgbot.handlers.router import admin_router


@admin_router.message(StateFilter(AddProduct.get_product_color))
async def get_product_color(message: types.Message, state: FSMContext):
    product_color = message.text
    if "/cancel" in product_color:
        await state.clear()
        await message.answer("Product adding has cancelled")
    else:
        await state.update_data(product_color=product_color)
        await message.answer("Enter product's ram amount")
        await state.set_state(AddProduct.get_product_ram)
