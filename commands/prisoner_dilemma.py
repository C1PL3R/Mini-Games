from aiogram import F, Router
from random import randint
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_i18n import I18nContext
from database import *

prisoner_dilemma_router = Router()

@prisoner_dilemma_router.message(Command("prisoner_dilemma"))
async def prisoner_dilemma_cmd(message: Message):
    await message.answer("Прочитайте правила перед грою /help!")
    