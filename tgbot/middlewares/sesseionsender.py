from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from tgbot.applecryptodb.apple_crypto_orm import DBCommands


class DBMiddleware(BaseMiddleware):
    def __init__(self, session):
        self.session = session

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data['repo'] = DBCommands(self.session)
        result = await handler(event, data)
        del data['repo']
        return result
