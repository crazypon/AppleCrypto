from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from tgbot.handlers.admin_handlers.resources import AddProduct
from tgbot.handlers.router import admin_router


@admin_router.message(StateFilter(AddProduct.get_product_category))
async def get_product_category(message: types.Message, state: FSMContext):
    product_category = message.text
    if product_category == "/cancel":
        await state.clear()
        await message.answer("Product adding has cancelled")
    else:
        await state.update_data(product_category=product_category)
        await message.answer("Enter product's subcategory")
        await state.set_state(AddProduct.get_product_subcategory)

