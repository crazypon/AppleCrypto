from aiogram.filters.state import State, StatesGroup


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
