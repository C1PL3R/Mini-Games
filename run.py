from aiogram import Bot, types
from aiogram.types.bot_command import BotCommand
from logging import INFO, basicConfig
import asyncio
import aiogram

from database import *
from config import TOKEN

from commands.tictactoe import router_ttt
from commands.start import router_start
from commands.quess_number import router_guess_number

from commands.dice import router_dice
from commands.score import router_score
from commands.shop import router_shop
from commands.change_skin import router_change_skin
from commands.lang import router_settings, i18n_middleware
from commands.top import router_top
from commands.buy import router_pay

from commands.tictactoe_online import router_test

# session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot(token=TOKEN)#, session=session)
dp = aiogram.Dispatcher()


async def main():
    command_list = [(BotCommand(command="start", description="Bot Launch 🤖")),
                (BotCommand(command="help", description="Help 🆘")),
                (BotCommand(command="lang", description="Set language 🌐")),
                (BotCommand(command="score", description="Star Count ⭐")),
                (BotCommand(command="stars", description="Premium-stars 🌟")),
                (BotCommand(command="about_premium", description="👑 About premium 👑")),
                (BotCommand(command="buy", description="Buy Premium 🛒")),
                (BotCommand(command="shop", description="Shop 🧺")),
                (BotCommand(command="top", description="Top 10 Chat Players 🔝")),
                (BotCommand(command="change_skin", description="Select Game Skin ❌⭕")),
                (BotCommand(command="a", description="----- Games -----")),
                (BotCommand(command="tictactoe_online", description="⭕ Tic Tac Toe ❌ ONLINE 🌐")),
                (BotCommand(command="tictactoe", description="⭕ Tic Tac Toe ❌")),
                (BotCommand(command="guess_number", description="🎲 Guess the Number 🎲")),
                (BotCommand(command="prisoner_dilemma", description="Prisoner's dilemma 🦹‍♂️"))
                (BotCommand(command="luck", description="🎰 Test Your Luck 🎰"))]


    
    dp.include_routers(router_start, router_settings, router_ttt, 
                       router_guess_number, router_dice, router_score, router_pay,
                       router_shop, router_top, router_change_skin,
                       router_test)
    
    await bot.set_my_description(description="Hi, do you want to play tic-tac-toe or guess the number or play basketball or football? Interested? If so, click the button!")
    await bot.set_my_short_description(short_description="If you have any questions, just contact @C1PL3R_admin 😉")
    await bot.set_my_commands(command_list)
    basicConfig(level=INFO)
    
    i18n_middleware.setup(dispatcher=dp)

    await dp.start_polling(bot)
    #types.chat_administrator_rights.ChatAdministratorRights(can_delete_messages=True, can_restrict_members=True, can_change_info=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Close connection with Telegram Servers")