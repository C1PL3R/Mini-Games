from aiogram.types import Message
from aiogram import Router, F, types, enums, Bot
from aiogram.utils.chat_action import ChatActionSender
from aiogram.filters import Command
import asyncio
from aiogram_i18n import I18nContext, LazyProxy
from database import *
from aiogram_i18n.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.types import InlineKeyboardButton as kb
from aiogram.types import InlineKeyboardMarkup as km


router_dice = Router()

TOKEN = "5957173294:AAEIgZLBSCXfZM9mfPTayI8KygPFiYQXL5Q"
bot = Bot(token=TOKEN)

list = [("🏀", 3),
        ("⚽", 3),
        ("🎲", 2.9),
        ("🎯", 2.5),
        ("🎳", 2.5),
        ("🎰", 1.2)]


@router_dice.message(Command("luck"))
async def lucky_cmd(message: Message, i18n: I18nContext):
    basketball = InlineKeyboardButton(text=LazyProxy("basketball_game"), switch_inline_query_current_chat="🏀")
    football = InlineKeyboardButton(text=LazyProxy("football_game"), switch_inline_query_current_chat="⚽")
    dice = InlineKeyboardButton(text=LazyProxy("dice_game"), switch_inline_query_current_chat="🎲")
    dart = InlineKeyboardButton(text=LazyProxy("dart_game"), switch_inline_query_current_chat="🎯")
    casino = InlineKeyboardButton(text=LazyProxy("casino_game"), switch_inline_query_current_chat="🎰")
    bowling = InlineKeyboardButton(text=LazyProxy("bowling_game"), switch_inline_query_current_chat="🎳")


    keyboard_dice = InlineKeyboardMarkup(inline_keyboard=[
        [basketball],
        [football],
        [dice],
        [dart],
        [bowling],
        [casino]
    ])

    await message.answer(text=i18n.get("select_game"), reply_markup=keyboard_dice)



@router_dice.inline_query()
async def inline_echo(inline_query: types.InlineQuery, i18n: I18nContext):
    query = inline_query.query
    results = []

    if query == "🏀" or query == i18n.get("bas"):
        article_basketball = types.InlineQueryResultArticle(
                    id="Basketball",
                    title=i18n.get("bas_title"),
                    description=i18n.get("bas_desc"),
                    input_message_content=types.InputTextMessageContent(message_text="🏀"), 
                    thumbnail_url="https://upload.wikimedia.org/wikipedia/commons/7/7a/Basketball.png", 
                    thumbnail_width=300, thumbnail_height=300)
        results = []
        results.append(article_basketball)
    
    elif query == "⚽" or query == i18n.get("foot"):
        article_soccer = types.InlineQueryResultArticle(
                    id="Football",
                    title=i18n.get("foot_title"),
                    description=i18n.get("foot_desc"),
                    input_message_content=types.InputTextMessageContent(message_text="⚽"), 
                    thumbnail_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Soccer_ball.svg/600px-Soccer_ball.svg.png", 
                    thumbnail_width=300, thumbnail_height=300)
        results = []
        results.append(article_soccer)

    elif query == "🎲" or query == i18n.get("dice"):
        article_dice = types.InlineQueryResultArticle(
                id="Dice",
                title=i18n.get("dice_title"),
                description=i18n.get("dice_desc"),
                input_message_content=types.InputTextMessageContent(message_text="🎲"), 
                thumbnail_url="https://kevan.org/images/liarsdice/die3.png", 
                thumbnail_width=300, thumbnail_height=300)
        results = []
        results.append(article_dice)

    elif query == "🎯" or query == i18n.get("dart"):
        article_dice = types.InlineQueryResultArticle(
                id="Darts",
                title=i18n.get("dart_title"),
                description=i18n.get("dart_desc"),
                input_message_content=types.InputTextMessageContent(message_text="🎯"), 
                thumbnail_url="https://pngimg.com/d/darts_PNG26.png")
        results = []
        results.append(article_dice)

    elif query == "🎳" or query == i18n.get("bow"):
        article_bowling = types.InlineQueryResultArticle(
                id="Bowling",
                title=i18n.get("bow_title"),
                description=i18n.get("bow_desc"),
                input_message_content=types.InputTextMessageContent(message_text="🎳"), 
                thumbnail_url="https://uk.oisans.com/wp-content/uploads/sites/2/wpetourisme/11417272-diaporama.jpg")
        results = []
        results.append(article_bowling)

    elif query == "🎰" or query == i18n.get("casino"):
        article_bowling = types.InlineQueryResultArticle(
                id="Casino",
                title=i18n.get("casino_title"),
                description=i18n.get("casino_desc"),
                input_message_content=types.InputTextMessageContent(message_text="🎰"), 
                thumbnail_url="https://media.istockphoto.com/id/817307644/vector/jackpot-slot-casino-machine-vector-one-arm-bandit.jpg?s=612x612&w=0&k=20&c=kX6YBt8SCFJCRYQ4cpyLZG0lMFVTTjVuhiVqeNSFdlI=")
        results = []
        results.append(article_bowling)


    await inline_query.answer(results=results)



for emoji, time in list:
    @router_dice.message(F.dice.emoji == emoji)
    async def dice_cmd(message: Message, i18n: I18nContext, emoji=emoji, time=time):
        cursor.execute("SELECT score FROM game WHERE id = ?", (message.from_user.id,))
        score = cursor.fetchone()[0]
        
        cursor.execute("SELECT x2_score FROM game WHERE id = ?", (message.from_user.id,))
        x2_score = cursor.fetchone()[0]
        
        userResult = message.dice.value
        if score >= 1:
            msg = await message.answer_dice(emoji=emoji)
            compResult = msg.dice.value
            chat_id = message.chat.id
            await bot.send_chat_action(action=enums.ChatAction.TYPING, chat_id=chat_id)
            await asyncio.sleep(time)
            if userResult > compResult: 
                if userResult == 64 or userResult == 1 or userResult == 22 or userResult == 43 and emoji == "🎰":
                    num = 2
                else:
                    num = 1
                    
                await message.reply(i18n.get("win_text_dice", total_score=x2_score * num), parse_mode="html")

                cursor.execute("UPDATE game SET score = ? WHERE id = ?", (score + (num * x2_score), message.from_user.id,))
                conn.commit()
            elif userResult < compResult:          
                await message.reply(i18n.get(f"lose_text_dice"), parse_mode="html")
                cursor.execute("UPDATE game SET score = ? WHERE id = ?", (score - 1, message.from_user.id,))
                conn.commit()
            else:
                await message.reply(i18n.get(f"draw_text_dice"), parse_mode="html")
        else:
            await message.reply(i18n.get("not_enough_stars"))
