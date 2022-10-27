from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from bitcoinlib.wallets import Wallet
from pycoingecko import CoinGeckoAPI
from web3 import Web3

from tgbot.handlers.router import user_router
from tgbot.handlers.user_handlers.resources import MethodCD, BuyItem, PaidCD, convert_to_crypto
from tgbot.payments.btc_payments import generate_new_bitcoin_key, check_btc_payment, NoEnoughMoney
from tgbot.payments.eth_payments import check_eth_payment
from tgbot.applecryptodb.apple_crypto_orm import DBCommands


def paid_keyboard(item_price: int, address: str, currency: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="paid", callback_data=PaidCD(item_price=item_price, address=address, currency=currency))
    return builder.as_markup()


@user_router.callback_query(MethodCD.filter())
async def send_address(call: types.CallbackQuery, callback_data: MethodCD, repo: DBCommands, config):
    # api for fetching current price of Crypto
    cg = CoinGeckoAPI()
    item_id = callback_data.item_id
    currency = callback_data.currency
    # price of item in dollars
    price = await repo.get_item_price(item_id=item_id)
    if currency == "bitcoin":

        # converting dollars to btc
        item_price = convert_to_crypto(cg=cg, price=price, currency="bitcoin")
        # generating new key
        new_key = generate_new_bitcoin_key(config)

        await call.message.answer(f"Send {item_price / 10 ** 8} BTC to the\n"
                                  f"<code>{new_key}</code> address", parse_mode="HTML",
                                  reply_markup=paid_keyboard(item_price=item_price, address=new_key, currency="btc"))

    else:
        # converting dollars to ether
        item_price = convert_to_crypto(cg=cg, price=price, currency="ethereum")
        eth_address = config['payments']['wallet_address_eth']
        await call.message.answer(f"Send {item_price / 10 ** 8} ETH to the\n"
                                  f"<code>{eth_address}</code> address", parse_mode="HTML",
                                  reply_markup=paid_keyboard(item_price=price, address=eth_address, currency="eth"))


@user_router.callback_query(PaidCD.filter())
async def check_address(call: types.CallbackQuery, state: FSMContext, repo: DBCommands, callback_data: PaidCD,):
    item_price = callback_data.item_price
    currency = callback_data.currency
    address = callback_data.address
    if currency == "btc":
        try:
            try:
                success = await check_btc_payment(address=address, price=item_price, repo=repo)
                if success:
                    await call.message.answer("<b>Payment Completed Successfully!!!</b>", parse_mode="HTML")
                    await repo.save_purchase_btc(call.from_user.id, address)
                    wallet = Wallet("amogus7")
                    wallet.transactions_update()
                    wallet.new_key()
                    wallet.scan()
                    wallet.send_to("tb1q30c3c6fe2dtuvewu5x7lus94fhl6kxmsde0yp9", amount=1000, fee=1024, offline=False)
                else:
                    await call.message.answer("Payment not confirmed or not found. Please try later")
                    return
            except IndexError:
                await call.message.answer("You have already paid for this product! Please "
                                          "buy new one using /buy command")
        except NoEnoughMoney:
            await call.message.answer("Your money is not enough!")
    else:
        await call.message.answer("Send transaction hash to check the payment")
        await state.update_data(item_price=item_price)
        await state.set_state(BuyItem.check_payment)


@user_router.message(StateFilter(BuyItem.check_payment))
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
        await repo.save_purchase_eth(message.from_user.id, str(tx_hash))
        await state.clear()






