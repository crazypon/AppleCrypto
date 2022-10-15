from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from bitcoinlib.wallets import Wallet
from pycoingecko.api import CoinGeckoAPI

from tgbot.handlers.router import user_router
from tgbot.handlers.user_handlers.resources import MethodCD, BuyItem, PaidCD
from tgbot.payments.btc_payments import generate_new_btc_wallet, check_btc_payment, NoEnoughMoney
from tgbot.payments.eth_payments import generate_new_eth_wallet, check_eth_payment
from tgbot.applecryptodb.apple_crypto_orm import DBCommands


def paid_keyboard(item_price: int, wallet_name: str, address: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="paid", callback_data=PaidCD(item_price=item_price, wallet_name=wallet_name,
                                                     address=address))
    return builder.as_markup()


@user_router.callback_query(MethodCD.filter())
async def send_address(call: types.CallbackQuery, callback_data: MethodCD, repo: DBCommands, state: FSMContext):
    cg = CoinGeckoAPI()  # api for getting current price of cryptocurrencies
    item_id = callback_data.item_id
    currency = callback_data.currency
    # price of item in dollars
    price = await repo.get_item_price(item_id=item_id)
    if currency == "bitcoin":
        # converting satoshi into bitcoin
        user_id = call.from_user.id

        # converting dollars to btc
        raw_btc_price = cg.get_price(ids="bitcoin", vs_currencies="usd")  # getting price of btc
        btc_price = raw_btc_price["bitcoin"]["usd"]
        raw_item_price = price / btc_price
        item_price = round(raw_item_price, 8)

        wallet_id = await repo.get_wallet_id(user_id)
        results = generate_new_btc_wallet(user_id, wallet_id)
        wallet_name = results["wallet_name"]

        # this address title for bitcoinlib will be for the next "invoice"
        await repo.save_wallet_id(user_id=user_id, wallet_id=results["next_wallet_id"])

        # generating address from Wallet obj
        key = results["wallet"].get_key()
        new_address = key.address

        await call.message.answer(f"Send {item_price:.8f} BTC to the\n"
                                  f"<code>{new_address}</code> address", parse_mode="HTML",
                                  reply_markup=paid_keyboard(item_price=price, wallet_name=wallet_name, address="none"))

        await state.set_state(BuyItem.check_payment)
    else:
        # converting dollars to btc
        raw_btc_price = cg.get_price(ids="ethereum", vs_currencies="usd")  # getting price of btc
        ethereum_price = raw_btc_price["ethereum"]["usd"]
        item_price = price / ethereum_price
        eth_address = generate_new_eth_wallet()
        await call.message.answer(f"Send {item_price} ETH to the\n"
                                  f"<code>{eth_address}</code> address", parse_mode="HTML",
                                  reply_markup=paid_keyboard(item_price=price, wallet_name="none", address=eth_address))


@user_router.callback_query(PaidCD.filter())
async def check_address(call: types.CallbackQuery, state: FSMContext, repo: DBCommands, callback_data: PaidCD):
    item_price = callback_data.item_price
    wallet_name = callback_data.wallet_name
    eth_address = callback_data.address
    if wallet_name != "none":
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
    else:
        tx_hash = check_eth_payment(address=eth_address, item_price=item_price)
        if tx_hash:
            await call.message.answer("<b>Payment Completed Successfully!!!</b>", parse_mode="HTML")
            await repo.save_purchase(call.from_user.id, str(tx_hash))
            await state.clear()







