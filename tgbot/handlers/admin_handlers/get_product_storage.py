from aiogram import types
from aiogram.fsm.context import FSMContext
from tgbot.handlers.admin_handlers.resources import AddProduct
from tgbot.handlers.router import admin_router


@admin_router.message(state=AddProduct.get_product_storage)
async def get_product_storage(message: types.Message, state: FSMContext):
    product_storage = message.text
    if "/cancel" in product_storage:
        await state.clear()
        await message.answer("Product adding has cancelled")
    else:
        if product_storage.isdigit():
            await state.update_data(product_storage=product_storage)
            await message.answer("Enter product's color")
            await state.set_state(AddProduct.get_product_color)
        else:
            await message.answer("The value must be entered in numbers! Please send product's storage amount again")
            return
