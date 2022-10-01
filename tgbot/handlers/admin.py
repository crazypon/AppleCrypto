import configparser

from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from tgbot.applecryptodb.apple_crypto_orm import DBCommands
from tgbot.middlewares.sesseionsender import DBMiddleware
from tgbot.applecryptodb.sql import create_pool


class AddProduct(StatesGroup):
    get_product_name = State()
    get_product_storage = State()
    get_product_color = State()
    get_product_ram = State()
    get_product_category = State()
    get_product_subcategory = State()
    get_product_gadget_name = State()
    get_product_price = State()
    get_product_photo = State()


config = configparser.ConfigParser()
config.read("bot.ini")

admin_router = Router()
# admin_router.message.middleware(DBMiddleware(await create_pool(
#     user=config["db"]["user"],
#     password=config["db"]["password"],
#     host=config["db"]["host"],
#     database=config["db"]["database"]
# )))


async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Hello! enter the product's name, please")
    await state.set_state(AddProduct.get_product_name)


async def get_product_name(message: types.Message, state: FSMContext):
    product_name = message.text
    await state.update_data(product_name=product_name)
    await message.answer("Enter product's storage amount")
    await state.set_state(AddProduct.get_product_storage)


async def get_product_storage(message: types.Message, state: FSMContext):
    product_storage = message.text
    if product_storage.isdigit():
        await state.update_data(product_storage=product_storage)
        await message.answer("Enter product's color")
        await state.set_state(AddProduct.get_product_color)
    else:
        await message.answer("The value must be entered in numbers! Please send product's storage amount again")
        return


async def get_product_color(message: types.Message, state: FSMContext):
    product_color = message.text
    await state.update_data(product_color=product_color)
    await message.answer("Enter product's ram amount")
    await state.set_state(AddProduct.get_product_ram)


async def get_product_ram(message: types.Message, state: FSMContext):
    product_ram = message.text
    if product_ram.isdigit():
        await state.update_data(product_ram=product_ram)
        await message.answer("Enter product's category")
        await state.set_state(AddProduct.get_product_category)
    else:
        await message.answer("The value must be entered in numbers! Please send product's ram amount again")
        return


async def get_product_category(message: types.Message, state: FSMContext):
    product_category = message.text
    await state.update_data(product_category=product_category)
    await message.answer("Enter product's subcategory")
    await state.set_state(AddProduct.get_product_subcategory)


async def get_product_subcategory(message: types.Message, state: FSMContext):
    product_subcategory = message.text
    await state.update_data(product_subcategory=product_subcategory)
    await message.answer("Enter subcategory's subcategory")
    await state.set_state(AddProduct.get_product_gadget_name)


async def get_product_gadget_name(message: types.Message, state: FSMContext):
    product_gadget_name = message.text
    await state.update_data(product_gadget_name=product_gadget_name)
    await message.answer("Enter product's price")
    await state.set_state(AddProduct.get_product_price)


async def get_product_price(message: types.Message, state: FSMContext):
    product_price = message.text
    if product_price.isdigit():
        await state.update_data(product_price=product_price)
        await message.answer("Send the photo of product")
        await state.set_state(AddProduct.get_product_photo)
    else:
        await message.answer("The value must be entered in numbers! Please send product's price again")
        return


async def get_product_photo(message: types.Message, state: FSMContext, repo: DBCommands):
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

admin_router.message.register(add_product, Command(commands=["add"]))
admin_router.message.register(get_product_name, state=AddProduct.get_product_name)
admin_router.message.register(get_product_storage, state=AddProduct.get_product_storage)
admin_router.message.register(get_product_ram, state=AddProduct.get_product_ram)
admin_router.message.register(get_product_color, state=AddProduct.get_product_color)
admin_router.message.register(get_product_category, state=AddProduct.get_product_category)
admin_router.message.register(get_product_subcategory, state=AddProduct.get_product_subcategory)
admin_router.message.register(get_product_gadget_name, state=AddProduct.get_product_gadget_name)
admin_router.message.register(get_product_price, state=AddProduct.get_product_price)
admin_router.message.register(get_product_photo, F.content_type.in_({"photo"}), state=AddProduct.get_product_photo)
