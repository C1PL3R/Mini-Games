from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from typing import Any
from aiogram.filters import Command
from aiogram_i18n import I18nContext, I18nMiddleware, LazyProxy
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore
from database import *

from aiogram_i18n.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)  

router_settings = Router()

locale = "uk"

button_uk = InlineKeyboardButton(text=LazyProxy("uk", flag="🇺🇦"), callback_data="ukrainian")
button_en = InlineKeyboardButton(text=LazyProxy("en", flag="🇬🇧") , callback_data="english")
button_pl = InlineKeyboardButton(text=LazyProxy("pl", flag="🇵🇱") , callback_data="polish")
button_it = InlineKeyboardButton(text=LazyProxy("it", flag="🇮🇹") , callback_data="Italian")


keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [button_uk],
    [button_en],
    [button_pl],
    [button_it]
])

@router_settings.message(Command("lang"))
async def cmd_start(message: Message, i18n: I18nContext) -> Any:
    await message.answer(text=i18n.get("select_language"), reply_markup=keyboard)

#lang_list = [("uk", "ukrainian"),("en", "english"), ("pl", "polish"), ("it", "Italian")]
lang_list = [("uk", "ukrainian"), ("en", "english")]

for language, lang_callback in lang_list:
    @router_settings.callback_query(F.data == lang_callback)
    async def set_lang(callback: CallbackQuery, i18n: I18nContext, language=language):
        global lang
        cursor.execute("UPDATE game SET lang = ? WHERE id = ?", (language, callback.from_user.id,))
        conn.commit()

        cursor.execute("SELECT lang FROM game WHERE id = ?", (callback.from_user.id,))
        lang_from_db = cursor.fetchone()[0]
        lang = lang_from_db
        await i18n.set_locale(lang)
        
        await callback.message.edit_text(text=i18n.get("the_language_has_been_changed"), reply_markup=keyboard)
        

i18n_middleware = I18nMiddleware(default_locale=locale, core=FluentRuntimeCore(path="lang/{locale}/"))

