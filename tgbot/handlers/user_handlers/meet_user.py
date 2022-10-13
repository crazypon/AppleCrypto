from aiogram import types
from aiogram.filters.command import Command
from sqlalchemy.exc import IntegrityError
from tgbot.applecryptodb.apple_crypto_orm import DBCommands
from tgbot.handlers.user_handlers.show_categories import user_router


@user_router.message(Command(commands=["start"]))
async def show_capabilities(message: types.Message, repo: DBCommands):
    sticker_id = "CAACAgIAAxkBAAICoWND53vAbeMkItNI6R59OxJm3Jg3AAJFAwACtXHaBpOIEByJ3A0bKgQ"
    await message.answer_sticker(sticker_id)
    await message.answer(
        "<b>Hello!👋</b>\n"
        "\n"
        "Use /buy - command to see\n"
        "what we have in our store✨!", parse_mode="HTML"
    )
    try:
        await repo.save_user(message.from_user.id)
    except IntegrityError:
        pass
