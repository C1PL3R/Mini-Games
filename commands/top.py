from aiogram import types, Router, F
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.filters import Command
from aiogram import Bot

from aiogram_i18n import I18nContext, LazyProxy
from aiogram_i18n.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
) 

from database import *

TOKEN = "5957173294:AAEIgZLBSCXfZM9mfPTayI8KygPFiYQXL5Q"
bot = Bot(token=TOKEN)

router_top = Router()

async def get_chat_member(i18n: I18nContext, message: types.Message,):
    cursor.execute("UPDATE game SET group_id = ? WHERE id = ?", (message.chat.id, message.from_user.id,))
    conn.commit()   
    cursor.execute("SELECT id FROM game WHERE group_id = ?", (message.chat.id,))
    result = cursor.fetchall()

    list_id = [row[0] for row in result]
    list_score = []

    for member in list_id:
        cursor.execute("SELECT score FROM game WHERE id = ?", (int(member),))
        score = cursor.fetchone()[0]
        list_score.append(score)

    id_score_pairs = list(zip(list_id, list_score))

    main_list = sorted(id_score_pairs, key=lambda x: x[1], reverse=True)
    main_list.sort(key=lambda x: x[1], reverse=True)

    a = 1
    main_text = ""
    main_list_10 = main_list[:10]
    
    for id, score in main_list_10:
        cursor.execute("SELECT name FROM game WHERE id = ?", (int(id),))
        name = cursor.fetchone()[0]

        text = f"{a}. {name} — <b>{score}</b> ⭐\n"
        main_text += text
        a += 1
    
    text1 = i18n.get("top_10")

    await message.answer(f"{text1}\n{main_text}", parse_mode="html")


@router_top.message(Command("top"))
async def top_cmd(message: types.Message, i18n: I18nContext):
    if message.chat.type == "supergroup" or message.chat.type == "group":
        await get_chat_member(i18n=i18n, message=message)
    else:
        button = InlineKeyboardButton(text=LazyProxy("add_bot_to_group"), url=f"https://t.me/mini_ggamesBot?startgroup=true")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [button]
        ])
        await message.answer(i18n.get("only_groups"), reply_markup=keyboard)


@router_top.message_reaction()
async def message_reaction_handler(message_reaction: types.MessageReactionUpdated):
    if message_reaction.chat.type == "private":
        chat_id = message_reaction.chat.id
        await bot.send_message(chat_id=chat_id, text=f"❤️")
        

# @router_top.error(ExceptionTypeFilter(Exception), F.update.message.as_("message"))
# async def handle_my_custom_exception(message: types.Message):
#     await message.answer("/start")

@router_top.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def add_member(chat_member: types.ChatMemberUpdated, i18n: I18nContext):
    user = chat_member.new_chat_member.user.is_bot
    if not user:
        cursor.execute("UPDATE game SET group_id = ? WHERE id = ?", (chat_member.chat.id, chat_member.new_chat_member.user.id,))
        conn.commit()   
        await chat_member.answer(i18n.get("new_chat_member", name=chat_member.new_chat_member.user.mention_html()), parse_mode="html")
    else:
        await chat_member.answer(i18n.get("new_chat_member", name=chat_member.new_chat_member.user.mention_html()), parse_mode="html")


async def get_chat_members_ids(chat_id):
    members = []
    m = 0
    return m


@router_top.message(Command("get_id"))
async def get_members(message: types.Message):
    chat_id = message.chat.id
    members_ids = await get_chat_members_ids(chat_id)
    await message.reply(f"Учасники чату та їх ідентифікатори: {await bot.get_chat_member(chat_id=chat_id, user_id=5588913711)}")
