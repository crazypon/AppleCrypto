from decimal import Decimal

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from bitcoinlib.wallets import Wallet
from bitcoinlib.values import Value

from tgbot.handlers.router import user_router
from tgbot.handlers.user_handlers.resources import MethodCD, BuyItem, PaidCD
from tgbot.handlers.user_handlers.ac_invoice import generate_new_btc_wallet, check_btc_payment, NoEnoughMoney
from tgbot.handlers.user_handlers.ac_invoice import generate_new_eth_wallet
from tgbot.applecryptodb.apple_crypto_orm import DBCommands


def paid_keyboard(item_price: int, wallet_name: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="paid", callback_data=PaidCD(item_price=item_price, wallet_name=wallet_name))
    return builder.as_markup()


@user_router.callback_query(MethodCD.filter())
async def send_address(call: types.CallbackQuery, callback_data: MethodCD, repo: DBCommands, state: FSMContext):
    item_id = callback_data.item_id
    currency = callback_data.currency
    # price of item
    price = await repo.get_item_price(item_id=item_id)
    if currency == "bitcoin":
        # converting satoshi into bitcoin
        human_price = Value(price, "sat").str(1)
        user_id = call.from_user.id

        wallet_id = await repo.get_wallet_id(user_id)
        results = generate_new_btc_wallet(user_id, wallet_id)
        wallet_name = results["wallet_name"]

        # this address title for bitcoinlib will be for the next "invoice"
        await repo.save_wallet_id(user_id=user_id, wallet_id=results["next_wallet_id"])

        # generating address from Wallet obj
        key = results["wallet"].get_key()
        new_address = key.address

        await call.message.answer(f"Send {human_price} to the\n"
                                  f"<code>{new_address}</code> address", parse_mode="HTML",
                                  reply_markup=paid_keyboard(item_price=price, wallet_name=wallet_name))

        await state.set_state(BuyItem.check_payment)
    else:
        eth_address = generate_new_eth_wallet()

        await state.update_data(eth_address=eth_address)
        await state.set_state(BuyItem.check_payment)






@user_router.callback_query(PaidCD.filter())
async def check_address(call: types.CallbackQuery, state: FSMContext, repo: DBCommands, callback_data: PaidCD):
    # TODO see what comes as a price than edit it because there is no satoshi just bitcoins that's bad
    item_price = callback_data.item_price
    wallet_name = callback_data.wallet_name

    wallet = Wallet(wallet_name)

    try:
        transaction_hash = check_btc_payment(wallet=wallet, item_price=item_price)
        if transaction_hash:
            await call.message.answer("<b>Payment Completed Successfully!!!</b>", parse_mode="HTML")
            await repo.save_purchase(call.from_user.id, str(transaction_hash))
            await state.clear()
        else:
            await call.message.answer("Payment not confirmed or not found. Please try later")
            return
    except NoEnoughMoney:
        await call.message.answer("Your money is not enough!")





