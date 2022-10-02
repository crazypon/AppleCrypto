from aiogram import types
from aiogram.fsm.context import FSMContext
from tgbot.handlers.admin_handlers.resources import AddProduct
from tgbot.handlers.router import admin_router


@admin_router.message(state=AddProduct.get_product_subcategory)
async def get_product_subcategory(message: types.Message, state: FSMContext):
    product_subcategory = message.text
    await state.update_data(product_subcategory=product_subcategory)
    await message.answer("Enter subcategory's subcategory")
    await state.set_state(AddProduct.get_product_gadget_name)
