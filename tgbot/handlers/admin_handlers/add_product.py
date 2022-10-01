from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from tgbot.handlers.admin_handlers.resources import AddProduct


add_product_router = Router()


@add_product_router.message(Command(commands=["add"]))
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Hello! enter the product's name, please")
    await state.set_state(AddProduct.get_product_name)