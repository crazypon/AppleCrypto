from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from tgbot.handlers.admin_handlers.resources import AddProduct


get_product_price_router = Router()


@get_product_price_router.message(state=AddProduct.get_product_price)
async def get_product_price(message: types.Message, state: FSMContext):
    product_price = message.text
    if product_price.isdigit():
        await state.update_data(product_price=product_price)
        await message.answer("Send the photo of product")
        await state.set_state(AddProduct.get_product_photo)
    else:
        await message.answer("The value must be entered in numbers! Please send product's price again")
        return
