from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from tgbot.handlers.admin_handlers.resources import AddProduct
from tgbot.handlers.router import admin_router


@admin_router.message(StateFilter(AddProduct.get_product_ram))
async def get_product_ram(message: types.Message, state: FSMContext):
    product_ram = message.text
    if "/cancel" in product_ram:
        await state.clear()
        await message.answer("Product adding has cancelled")
    else:
        if product_ram.isdigit():
            await state.update_data(product_ram=product_ram)
            await message.answer("Enter product's category")
            await state.set_state(AddProduct.get_product_category)
        else:
            await message.answer("The value must be entered in numbers! Please send product's ram amount again")
            return
