from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram_i18n import I18nContext, I18nMiddleware, LazyProxy
from database import *
from aiogram_i18n.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
) 

router_start = Router()



async def add_user_to_db(message: Message):
    username = message.from_user.username
    telegram_id = message.from_user.id
    user_full_telegram = message.from_user.full_name
    cursor.execute("SELECT * FROM game WHERE id = ?", (telegram_id,))
    record = cursor.fetchone()
    
    cursor.execute("SELECT * FROM skins WHERE id = ?", (telegram_id,))
    record1 = cursor.fetchone()

    cursor.execute("SELECT * FROM game WHERE group_id = ?", (message.chat.id,))
    record2 = cursor.fetchone()

    cursor.execute("SELECT * FROM online WHERE id = ?", (message.chat.id,))
    record3 = cursor.fetchone()

    if message.chat.type == "private" or message.chat.type == "supergroup" or message.chat.type == "group":
        if record is None:
            if message.chat.type == "supergroup" or message.chat.type == "group":
                cursor.execute("INSERT INTO game (id, name, link, group_id) VALUES (?, ?, ?, ?)", (telegram_id, user_full_telegram, username, message.chat.id))
                conn.commit()
            else:
                cursor.execute("INSERT INTO game (id, name, link) VALUES (?, ?, ?)", (telegram_id, user_full_telegram, username))
                conn.commit()
        else:
            if record[1] != user_full_telegram or record[1] != username:
                cursor.execute("UPDATE game SET name = ?, link = ? WHERE id = ?", (user_full_telegram, username, telegram_id,))
                conn.commit()
        
        if record1 is None:
            cursor.execute("INSERT INTO skins (id) VALUES (?)", (telegram_id,))
            conn.commit()

        if record3 is None:
            cursor.execute("INSERT INTO online (id, name) VALUES (?, ?)", (telegram_id, user_full_telegram,))
            conn.commit()
        else:
            cursor.execute("INSERT INTO online (id, name) VALUES (?, ?)", (telegram_id, user_full_telegram))
            conn.commit()
        

    if message.chat.type == "supergroup" or message.chat.type == "group":
        if record2 is None:
            cursor.execute("INSERT INTO game (group_id, group_name, group_link) VALUES (?, ?, ?)",(message.chat.id, message.chat.title, message.chat.username,))
            conn.commit()
        else:
            if record2[1] != message.chat.title or record[1] != message.chat.username:
                cursor.execute("UPDATE game SET group_name = ?, group_link = ? WHERE group_id = ?",(message.chat.title, message.chat.username, message.chat.id,))
                conn.commit()


async def add_user_to_db_in_group(message: Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        cursor.execute("SELECT * FROM game WHERE group_id = ?", (message.chat.id,))
        record2 = cursor.fetchone()
        if record2 is None:
            cursor.execute("UPDATE game SET group_id = ? WHERE id = ?", (message.chat.id, message.from_user.id,))
            conn.commit()        

nl = "\n"

@router_start.message(CommandStart())
async def start(message: Message, i18n: I18nContext):
    await add_user_to_db(message)
    await add_user_to_db_in_group(message)

    button = InlineKeyboardButton(text=LazyProxy("add_bot_to_group"), url=f"https://t.me/mini_ggamesBot?startgroup=true")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [button]
    ])
    await message.answer(i18n.get("start_message", user=message.from_user.mention_html(), nl=nl), parse_mode="html", reply_markup=keyboard)


@router_start.message(Command('help'))
async def help(message: Message, i18n: I18nContext):
    await message.answer(i18n.get("help_message", nl=nl), parse_mode="html")

@router_start.message(Command('about_premium'))
async def about_premium(message: Message, i18n: I18nContext):
    await message.answer(i18n.get("about_premium", nl=nl), parse_mode="html")