import datetime

from sqlalchemy import BigInteger, Integer, SmallInteger, String, Column, ForeignKey, delete, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.future import select
from sqlalchemy import update


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
    photo_id = Column(String())

    def __repr__(self):
        product_description = f"Model: {Product.name}\n"\
                              f"Price: ${Product.price}\n"\
                              f"storage: {Product.storage} GB\n"\
                              f"ram: {Product.ram} GB"
        return product_description


class Customer(Base):
    __tablename__ = "customers"
    id = Column(BigInteger(), primary_key=True)
    user_id = Column(Integer(), unique=True)
    wallet_id = Column(SmallInteger(), default=0)


class BTCPayment(Base):
    __tablename__ = "btc_payments"
    id = Column(BigInteger(), primary_key=True)
    user_id = Column(BigInteger(), ForeignKey('customers.user_id'))
    transaction_key = Column(String(), unique=True)
    relationship_for_customer = relationship("Customer")


class ETHPayment(Base):
    __tablename__ = "eth_payments"
    id = Column(BigInteger(), primary_key=True)
    user_id = Column(BigInteger(), ForeignKey('customers.user_id'))
    transaction_hash = Column(String(), unique=True)
    relationship_for_customer = relationship("Customer")


class ReservedAddress(Base):
    __tablename__ = "reserved_addresses"
    id = Column(BigInteger(), primary_key=True)
    user_id = Column(BigInteger())
    eth_address = Column(String())
    reserved_time = Column(DateTime(), default=datetime.datetime.now())


class DBCommands:
    def __init__(self, session):
        self.session = session

    # ------------------------Product Methods----------------------------
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
        stmt = select(Product.id, Product.name, Product.price, Product.storage, Product.ram, Product.color,
                      Product.photo_id).where(
            Product.category == category,
            Product.subcategory == subcategory,
            Product.gadget_name == gadget_name
        )
        stmt = await self.session.execute(stmt)
        return stmt

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

    async def get_item_price(self, item_id):
        stmt = select(Product.price).where(Product.id == item_id)
        stmt = await self.session.execute(stmt)
        val = stmt.scalar()
        return val

    # --------------------Customer Methods-------------------

    async def save_user(self, user_id):
        self.session.add(Customer(user_id=user_id))
        await self.session.commit()

    # -------------------ETHPayment Methods--------------------

    async def save_purchase_eth(self, user_id: int, tx_hash: str):
        self.session.add(ETHPayment(user_id=user_id, transaction_hash=tx_hash))
        await self.session.commit()

    async def get_transaction_hash_eth(self, tx_hash: str):
        stmt = select(ETHPayment.transaction_hash).where(ETHPayment.transaction_hash == tx_hash)
        stmt = await self.session.execute(stmt)
        val = stmt.scalar()
        return val

    # ----------------------BTCPayments-----------------------
    async def save_purchase_btc(self, user_id: int, key: str):
        self.session.add(BTCPayment(user_id=user_id, transaction_key=key))
        await self.session.commit()

    async def get_key_from_db(self, key: str):
        stmt = select(BTCPayment.transaction_key).where(BTCPayment.transaction_key == key)
        stmt = await self.session.execute(stmt)
        val = stmt.scalar()
        return val

    # ----------------------ReservedAddress Methods ------------------------------

    async def check_reserved_address(self, eth_addr: str):
        stmt = select(ReservedAddress.eth_address).where(ReservedAddress.eth_address == eth_addr)
        stmt = await self.session.execute(stmt)
        val = stmt.scalar()
        return val

    async def reserve_address(self, user_id: int, eth_addr: str):
        address = await self.check_reserved_address(eth_addr)
        if address:
            return False
        else:
            self.session.add(ReservedAddress(user_id=user_id, eth_address=eth_addr))
            await self.session.commit()
            return True

    async def remove_from_reserve(self, eth_addr: str):
        print("address removed successfully")
        stmt = delete(ReservedAddress).where(ReservedAddress.eth_address == eth_addr)
        await self.session.execute(stmt)
        await self.session.commit()


