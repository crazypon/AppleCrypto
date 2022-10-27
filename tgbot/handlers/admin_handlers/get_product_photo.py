from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from tgbot.handlers.admin_handlers.resources import AddProduct
from tgbot.applecryptodb.apple_crypto_orm import DBCommands
from tgbot.handlers.router import admin_router


@admin_router.message(StateFilter(AddProduct.get_product_photo))
async def get_product_photo(message: types.Message, state: FSMContext, repo: DBCommands):
    if "/cancel" in message.text:
        await state.clear()
        await message.answer("Product adding has cancelled")
    else:
        photo_id = message.photo[-1].file_id
        product_data = await state.get_data()
        await repo.save_product(
            name=product_data["product_name"],
            storage=product_data["product_storage"],
            ram=product_data["product_ram"],
            color=product_data["product_color"],
            category=product_data["product_category"],
            subcategory=product_data["product_subcategory"],
            gadget_name=product_data["product_gadget_name"],
            price=int(product_data["product_price"]),
            photo_id=photo_id
        )
        await message.answer("Product successfully has added to database!")
        await state.clear()
