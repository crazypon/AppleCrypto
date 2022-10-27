from aiogram import Router
from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Union


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id == 1231974448:
            return True
        else:
            return False


user_router = Router()
admin_router = Router()
admin_router.message.filter(
    AdminFilter()
)
