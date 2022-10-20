from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from bitcoinlib.wallets import Wallet
from pycoingecko.api import CoinGeckoAPI
from web3 import Web3

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

    else:
        # converting dollars to btc
        raw_btc_price = cg.get_price(ids="ethereum", vs_currencies="usd")  # getting price of btc
        ethereum_price = raw_btc_price["ethereum"]["usd"]
        item_price = price / ethereum_price
        # eth_address = generate_new_eth_wallet()
        eth_address = "0xCE2c3B44843c28de7418770c385B85A4E208AAd5"
        await call.message.answer(f"Send {item_price} ETH to the\n"
                                  f"<code>{eth_address}</code> address", parse_mode="HTML",
                                  reply_markup=paid_keyboard(item_price=price, wallet_name="none", address=eth_address))


@user_router.callback_query(PaidCD.filter())
async def check_address(call: types.CallbackQuery, state: FSMContext, repo: DBCommands, callback_data: PaidCD,
                        web3: Web3):
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
            else:
                await call.message.answer("Payment not confirmed or not found. Please try later")
                return
        except NoEnoughMoney:
            await call.message.answer("Your money is not enough!")
    else:
        await call.message.answer("Send transaction hash to check the payment")
        await state.update_data(item_price=item_price)
        await state.set_state(BuyItem.check_payment)


@user_router.message(state=BuyItem.check_payment)
async def get_transaction_hash(message: types.Message, web3: Web3, state: FSMContext, repo: DBCommands, config):
    tx_data = await state.get_data()
    item_price = tx_data["item_price"]
    tx_hash = message.text
    try:
        await check_eth_payment(item_price=item_price, tx_hash=tx_hash, web3=web3, config=config, repo=repo)

    except EOFError:
        await message.answer("This transaction hash is from previous purchase. Please send the transaction hash of "
                             "current purchase")

    except IndexError:
        await message.answer(f"This transaction hash has wrong recipient. Please send the transaction hash where "
                             f"recipient's address is {config['payments']['wallet_address_eth']}")

    except ValueError:
        await message.answer("No enough money sent!")

    else:
        await message.answer("<b>Payment Completed Successfully!!!</b>", parse_mode="HTML")
        await repo.save_purchase(message.from_user.id, str(tx_hash))
        await state.clear()






