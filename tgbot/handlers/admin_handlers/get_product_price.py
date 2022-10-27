from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from tgbot.handlers.admin_handlers.resources import AddProduct
from tgbot.handlers.router import admin_router


@admin_router.message(StateFilter(AddProduct.get_product_price))
async def get_product_price(message: types.Message, state: FSMContext):
    product_price = message.text
    if "/cancel" in product_price:
        await state.clear()
        await message.answer("Product adding has cancelled")
    else:
        if product_price.isdigit():
            await state.update_data(product_price=product_price)
            await message.answer("Send the photo of product")
            await state.set_state(AddProduct.get_product_photo)
        else:
            await message.answer("The value must be entered in numbers! Please send product's price again")
            return
