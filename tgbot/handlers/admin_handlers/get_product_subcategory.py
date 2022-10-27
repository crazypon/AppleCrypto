from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from tgbot.handlers.admin_handlers.resources import AddProduct
from tgbot.handlers.router import admin_router


@admin_router.message(StateFilter(AddProduct.get_product_subcategory))
async def get_product_subcategory(message: types.Message, state: FSMContext):
    product_subcategory = message.text
    if "/cancel" in product_subcategory:
        await state.clear()
        await message.answer("Product adding has cancelled")
    else:
        await state.update_data(product_subcategory=product_subcategory)
        await message.answer("Enter subcategory's subcategory")
        await state.set_state(AddProduct.get_product_gadget_name)
