from aiogram import types
from aiogram.fsm.context import FSMContext
from tgbot.handlers.admin_handlers.resources import AddProduct
from tgbot.handlers.router import admin_router


@admin_router.message(state=AddProduct.get_product_category)
async def get_product_category(message: types.Message, state: FSMContext):
    product_category = message.text
    await state.update_data(product_category=product_category)
    await message.answer("Enter product's subcategory")
    await state.set_state(AddProduct.get_product_subcategory)

