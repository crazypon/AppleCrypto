from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from tgbot.handlers.admin_handlers.resources import AddProduct

get_product_name_router = Router()


@get_product_name_router.message(state=AddProduct.get_product_name)
async def get_product_name(message: types.Message, state: FSMContext):
    product_name = message.text
    await state.update_data(product_name=product_name)
    await message.answer("Enter product's storage amount")
    await state.set_state(AddProduct.get_product_storage)
