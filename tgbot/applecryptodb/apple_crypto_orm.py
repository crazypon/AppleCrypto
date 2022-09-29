from sqlalchemy import Integer, String, Column, ForeignKey, delete
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.future import select


Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    storage = Column(String())
    ram = Column(String())
    color = Column(String())
    category = Column(String())
    subcategory = Column(String())
    gadget_name = Column(String())
    price = Column(Integer())

    def __repr__(self):
        product_description = f"Model: {Product.name}\n"\
                              f"Price: ${Product.price}\n"\
                              f"storage: {Product.storage} GB\n"\
                              f"ram: {Product.ram} GB"
        return product_description


class DBCommands:
    def __init__(self, session):
        self.session = session
    
    async def get_all_categories(self):
        stmt = select(Product.category)
        stmt = await self.session.execute(stmt)
        val = stmt.all()

        return val
    
    async def get_all_subcategories(self, category):
        stmt = select(Product.subcategory).where(Product.category == category)
        stmt = await self.session.execute(stmt)
        val = stmt.all()
        return val

    async def get_all_gadget_names(self, category, subcategory):
        stmt = select(Product.gadget_name).where(Product.category == category).where(Product.subcategory == subcategory)
        stmt = await self.session.execute(stmt)
        val = stmt.all()
        return val

    async def get_all_items(self, category, subcategory, gadget_name):
        stmt = select(Product).where(Product.category == category).where(Product.subcategory == subcategory)
        stmt = stmt.where(Product.gadget_name == gadget_name)
        stmt = await self.session.execute(stmt)
        val = stmt.all()
        return val

    async def get_all_item_ids(self, category, subcategory, gadget_name):
        stmt = select(Product.id).where(Product.category == category).where(Product.subcategory == subcategory)
        stmt = stmt.where(Product.gadget_name == gadget_name)
        stmt = await self.session.execute(stmt)
        val = stmt.all()
        return val

    async def save_product(self, name, storage, ram, color, category, subcategory, gadget_name, price, photo_id):
        self.session.add(Product(
            name=name,
            storage=storage,
            ram=ram,
            color=color,
            category=category,
            subcategory=subcategory,
            gadget_name=gadget_name,
            price=price,
            photo_id=photo_id
        ))
        await self.session.commit()

