# from typing import Union
# from aiogram import F, Router, types
# from aiogram.filters.command import Command
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from aiogram.exceptions import TelegramBadRequest
# from tgbot.applecryptodb.apple_crypto_orm import DBCommands
# from tgbot.my_callback_data.apple_crypto_cd import NavigationCD, BuyCD
#
#
# user_router = Router()
#
#
# def make_callback_data(level, category="0", subcategory="0", gadget_name="0"):
#     return NavigationCD(current_level=level, category=category, subcategory=subcategory, gadget_name=gadget_name)
#
#
# async def categories_keyboard(repo: DBCommands):
#     current_level = 1
#     builder = InlineKeyboardBuilder()
#     category_names = await repo.get_all_categories()
#     amount_of_buttons = 0
#     for item in set(category_names):
#         category_name = item[0]
#         builder.button(text=f"{category_name} 🍏", callback_data=make_callback_data(level=current_level + 1,
#                                                                                   category=category_name))
#         amount_of_buttons += 1
#     if amount_of_buttons % 2 == 1:
#         builder.adjust(2)
#     elif amount_of_buttons % 3 == 1:
#         builder.adjust(3)
#     category_keyboard = builder.as_markup()
#     return category_keyboard
#
#
# async def subcategories_keyboard(category: str, repo: DBCommands):
#     current_level = 2
#     builder = InlineKeyboardBuilder()
#     subcategories = await repo.get_all_subcategories(category)
#     amount_of_buttons = 1
#     for item in set(subcategories):
#         subcategory_name = item[0]
#         builder.button(text=subcategory_name, callback_data=make_callback_data(level=current_level + 1,
#                                                                                category=category,
#                                                                                subcategory=subcategory_name))
#         amount_of_buttons += 1
#
#     builder.button(text="⬅️ Back",
#                    callback_data=make_callback_data(level=current_level - 1, category=category))
#     if amount_of_buttons % 2 == 1:
#         builder.adjust(2)
#     elif amount_of_buttons % 3 == 1:
#         builder.adjust(3)
#     subcategories_kb = builder.as_markup()
#     return subcategories_kb
#
#
# async def gadget_names_keyboard(category: str, subcategory: str, repo: DBCommands):
#     current_level = 3
#     builder = InlineKeyboardBuilder()
#     gadget_names = await repo.get_all_gadget_names(category, subcategory)
#     amount_of_buttons = 1
#     for item in set(gadget_names):
#         gadget_title = item[0]
#         builder.button(text=gadget_title, callback_data=make_callback_data(level=current_level + 1,
#                                                                            category=category,
#                                                                            subcategory=subcategory,
#                                                                            gadget_name=gadget_title))
#         amount_of_buttons += 1
#     builder.button(text="⬅️ Back", callback_data=make_callback_data(
#         level=current_level - 1,
#         category=category,
#         subcategory=subcategory
#     ))
#     if amount_of_buttons % 2 == 1:
#         builder.adjust(2)
#     elif amount_of_buttons % 3 == 1:
#         builder.adjust(3)
#     return builder.as_markup()
#
#
# async def show_all_items(call: types.CallbackQuery, repo: DBCommands, category: str, subcategory: str,
#                          gadget_name: str):
#     await call.message.answer("Here are our searching results!")
#     current_level = 4
#     items = await repo.get_all_items(category, subcategory, gadget_name)
#     for item in items:
#         message_format = f"Model: {item[1]}\n" \
#                          f"Price: ${item[2]}\n" \
#                          f"\n" \
#                          f"Storage: {item[3]} GB\n" \
#                          f"Ram: {item[4]} GB\n" \
#                          f"Color: {item[5]}"
#         builder = InlineKeyboardBuilder()
#         builder.button(text="Buy💸", callback_data=BuyCD(item_id=int(item[0])))
#         builder.button(text="⬅️ Back", callback_data=make_callback_data(
#             level=current_level - 1,
#             category=category,
#             subcategory=subcategory,
#             gadget_name=gadget_name
#         ))
#         item_keyboard = builder.as_markup()
#         await call.message.answer_photo(photo=item[6], caption=message_format, reply_markup=item_keyboard)
#
#
# async def show_categories(message: Union[types.Message, types.CallbackQuery], repo: DBCommands, **kwargs):
#     if isinstance(message, types.Message):
#         await message.answer("Hello! choose what you want to buy", reply_markup=await categories_keyboard(repo))
#     elif isinstance(message, types.CallbackQuery):
#         call = message
#         await call.message.edit_reply_markup(await categories_keyboard(repo))
#
#
# async def show_subcategories(call: types.CallbackQuery, repo: DBCommands, category, **kwargs):
#     await call.message.edit_text("What you want to buy")
#     await call.message.edit_reply_markup(await subcategories_keyboard(repo=repo, category=category))
#
#
# async def show_gadget_names(call: types.CallbackQuery, repo: DBCommands, category, subcategory, **kwargs):
#     try:
#         await call.message.edit_text("Which generation you want to buy?")
#         await call.message.edit_reply_markup(await gadget_names_keyboard(category=category,
#                                                                          subcategory=subcategory,
#                                                                          repo=repo))
#     except TelegramBadRequest:
#         await call.message.answer("Which generation you want to buy?",
#                                   reply_markup=await gadget_names_keyboard(category=category,
#                                                                            subcategory=subcategory,
#                                                                            repo=repo))
#
#
# async def navigate(call: types.CallbackQuery, callback_data: NavigationCD, repo: DBCommands):
#     level = callback_data.current_level
#     handlers = {
#         "1": show_categories,
#         "2": show_subcategories,
#         "3": show_gadget_names,
#         "4": show_all_items
#     }
#     handler = handlers[str(level)]
#     await handler(
#         call,
#         repo,
#         category=callback_data.category,
#         subcategory=callback_data.subcategory,
#         gadget_name=callback_data.gadget_name
#     )
#
# user_router.message.register(show_categories, Command(commands=["buy"]))
# user_router.callback_query.register(navigate, NavigationCD.filter())
