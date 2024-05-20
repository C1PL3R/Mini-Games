from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton as ikb
from aiogram.types import InlineKeyboardMarkup as ikm
from aiogram import F, Router
import asyncio
import random
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from database import *
from aiogram_i18n import I18nContext
from aiogram_i18n.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)  


router_ttt = Router()


button1 = InlineKeyboardButton(text="  ", callback_data="button1")
button2 = InlineKeyboardButton(text="  ", callback_data="button2")
button3 = InlineKeyboardButton(text="  ", callback_data="button3")

button4 = InlineKeyboardButton(text="  ", callback_data="button4")
button5 = InlineKeyboardButton(text="  ", callback_data="button5")
button6 = InlineKeyboardButton(text="  ", callback_data="button6")

button7 = InlineKeyboardButton(text="  ", callback_data="button7")
button8 = InlineKeyboardButton(text="  ", callback_data="button8")
button9 = InlineKeyboardButton(text="  ", callback_data="button9")


keyboard_ttt = InlineKeyboardMarkup(inline_keyboard=[
    [button1, button2, button3],
    [button4, button5, button6],
    [button7, button8, button9]
])

user_symbol = ""
compSymbol = ""

skin_user_X = ""
skin_user_Zero = ""

skin_comp_X = ""
skin_comp_Zero = ""

game = 0

a = "" 

button_list = [button1, button2, button3, button4, button5, button6, button7, button8, button9]         

attemps = 1

@router_ttt.message(Command('tictactoe'))
async def tictactoe(message: Message, i18n: I18nContext):   
    cursor.execute("SELECT skin FROM game WHERE id = ?", (message.from_user.id,))
    skin = cursor.fetchone()[0]  
    global button1, button2, button3, button4, button5, button6, button7, button8, button9, user_symbol, a, button_list, skin_user_Zero, skin_user_X, skin_comp_Zero, skin_comp_X, attemps
    
    if skin == "standart": 
        skin_user_X = "❌"
        skin_user_Zero = "⭕"

        skin_comp_X = "❌"
        skin_comp_Zero = "⭕"
    elif skin == "basketball_ball":
        skin_user_X = "🏀"
        skin_user_Zero = "🟠"

        skin_comp_X = "🏀"
        skin_comp_Zero = "🟠"
    elif skin == "soccer_ball":
        skin_user_X = "⚽"
        skin_user_Zero = "⚪"

        skin_comp_X = "⚽"
        skin_comp_Zero = "⚪"
    elif skin == "volleyball_ball":
        skin_user_X = "🏐"
        skin_user_Zero = "⚪"

        skin_comp_X = "🏐"
        skin_comp_Zero = "⚪"
    elif skin == "football_ball":
        skin_user_X = "🏈"
        skin_user_Zero = "🟤"

        skin_comp_X = "🏈"
        skin_comp_Zero = "🟤"
    elif skin == "fire":
        skin_user_X = "🔥"
        skin_user_Zero = "🟠"

        skin_comp_X = "🔥"
        skin_comp_Zero = "🟠"
    elif skin == "note":
        skin_user_X = "🎵"
        skin_user_Zero = "⚫"

        skin_comp_X = "🎵"
        skin_comp_Zero = "⚫"
    elif skin == "snow":
        skin_user_X = "❄️"
        skin_user_Zero = "🔵"

        skin_comp_X = "❄️"
        skin_comp_Zero = "🔵"
    elif skin == "sword":
        skin_user_X = "⚔️"
        skin_user_Zero = "🔘"

        skin_comp_X = "⚔️"
        skin_comp_Zero = "🔘"
    elif skin == "fire_heart":
        skin_user_X = "❤️‍🔥"
        skin_user_Zero = "🔴"

        skin_comp_X = "❤️‍🔥"
        skin_comp_Zero = "🔴"
    elif skin == "purple_heart":
        skin_user_X = "💖"
        skin_user_Zero = "🟣"

        skin_comp_X = "💖"
        skin_comp_Zero = "🟣"
    elif skin == "table_tennis":
        skin_user_X = "🏓"
        skin_user_Zero = "🔴"

        skin_comp_X = "🏓"
        skin_comp_Zero = "🔴"
    elif skin == "trophy":
        skin_user_X = "🏆"
        skin_user_Zero = "🌕"

        skin_comp_X = "🏆"
        skin_comp_Zero = "🌕"
    elif skin == "poo":
        skin_user_X = "💩"
        skin_user_Zero = "🟤"

        skin_comp_X = "💩"
        skin_comp_Zero = "🟤"
    elif skin == "star":
        skin_user_X = "⭐️"
        skin_user_Zero = "🌝"

        skin_comp_X = "⭐️"
        skin_comp_Zero = "🌝"
    elif skin == "premium_star":
        skin_user_X = "🌟"
        skin_user_Zero = "🤩"

        skin_comp_X = "🌟"
        skin_comp_Zero = "🤩" 




    attemps = 1

    buttons_list = [(button1), (button2), (button3), (button4), (button5), (button6), (button7), (button8), (button9)]
    for btn in buttons_list:
        btn.text = "  "
   
    
    buttonX = ikb(text=skin_comp_X, callback_data="cross")
    buttonZero = ikb(text=skin_comp_Zero, callback_data="zero")
    
    if game == 1:
        if user_symbol == skin_user_X:
            await message.answer(i18n.get("finish_game_cross"), reply_markup=keyboard_ttt)
        if user_symbol == skin_user_Zero:
            await message.answer(i18n.get("finish_game_zero"), reply_markup=keyboard_ttt)
    else:
        keyboardXandZero = ikm(inline_keyboard=[
            [buttonX, buttonZero]
        ])
        await message.answer(text=i18n.get("choose_who_you_will_be"), parse_mode="html", reply_markup=keyboardXandZero)
        
        

    @router_ttt.callback_query(F.data == "cross")
    async def callback_cross(callback: CallbackQuery, i18n: I18nContext):
        global user_symbol, game, compSymbol, compSymbol, user_symbol
        cursor.execute("SELECT lang FROM game WHERE id = ?", (callback.from_user.id,))
        lang = cursor.fetchone()[0]
        user_symbol = skin_user_X
        compSymbol = skin_comp_Zero
        game = 1
            
        await callback.message.edit_text(i18n.get("you_are_a_cross"), reply_markup=keyboard_ttt)
        
    @router_ttt.callback_query(F.data == "zero")
    async def callback_zero(callback: CallbackQuery, i18n: I18nContext):
        global user_symbol, game, compSymbol, skin_user_Zero, skin_comp_X, compSymbol, user_symbol
        
        game = 1
        user_symbol = skin_user_Zero
        compSymbol = skin_comp_X
        
        await callback.message.edit_text(i18n.get("you_are_a_zero"), reply_markup=keyboard_ttt)
    
 
buttons_list = [(button1, "button1"), (button2, "button2"), (button3, "button3"), (button4, "button4"), (button5, "button5"), (button6, "button6"), (button7, "button7"), (button8, "button8"), (button9, "button9")]

text = ""
win2 = 0



for button, callback_data in buttons_list:
    @router_ttt.callback_query(F.data == callback_data)
    async def ttt_callback(callback: CallbackQuery, i18n: I18nContext, btn=button):
        global user_symbol, text, win2, attemps
        cursor.execute("SELECT lang FROM game WHERE id = ?", (callback.from_user.id,))
        lang = cursor.fetchone()[0]
        
        if win2 == 1 or win2 == 2:
            pass
        else:
            if btn.text == "  ":
                if attemps == 1:
                    btn.text = user_symbol
                    attemps = 0
                    text = i18n.get("tictactoe_game")
                    win2 = 3
                    await asyncio.sleep(0.4)
                    await compGoes()
                else:
                    text = i18n.get("its_not_your_turn_now")
            else:
                text = i18n.get("this_cell_is_full")
            try:
                if win2 == 3:
                    await callback.message.edit_text(text, reply_markup=keyboard_ttt)
                else:
                    if win2 == 2:
                        await callback.message.edit_text(i18n.get("lose_text"), reply_markup=keyboard_ttt)
                    else:
                        await callback.message.edit_text(i18n.get("win_text"), reply_markup=keyboard_ttt)
            except TelegramBadRequest:
                pass
            await check_win(i18n=i18n, callback=callback)
        

async def compGoes():
    global button1, button2, button3, button4, button5, button6, button7, button8, button9, compSymbol, user_symbol, skin_user_X, skin_user_Zero, attemps
    button_list = [button1, button2, button3, button4, button5, button6, button7, button8, button9]

    # Filter out buttons with "X" or "O"
    available_buttons = [btn for btn in button_list if btn.text not in [skin_user_X, skin_user_Zero]]

    if available_buttons:
        list_compGoes = [
            (button1, button2, button3),
            (button4, button5, button6),
            (button7, button8, button9),
            (button1, button4, button7),
            (button2, button5, button8),
            (button3, button6, button9),
            (button1, button5, button9),
            (button7, button5, button3)
        ]

        comp_choice = None

        # Check for winning move
        for button_group in list_compGoes:
            comp_choice = check_and_choose_button(button_group, compSymbol, available_buttons)
            if comp_choice:
                comp_choice.text = compSymbol
                attemps = 1
                break

        # If no winning move, block user's winning move
        if not comp_choice:
            for button_group in list_compGoes:
                comp_choice = check_and_choose_button(button_group, user_symbol, available_buttons)
                if comp_choice:
                    comp_choice.text = compSymbol
                    attemps = 1
                    break

        # If neither winning nor blocking move, make a random move
        if not comp_choice:
            comp_choice = random.choice(available_buttons)
            comp_choice.text = compSymbol
            attemps = 1

def check_and_choose_button(button_group, symbol, available_buttons):
    button_texts = [button.text for button in button_group]
    if button_texts.count(symbol) == 2 and "  " in button_texts:
        return available_buttons[button_texts.index("  ")]
    return None


async def check_win(i18n: I18nContext, callback):
    global button1, button2, button3, button4, button5, button6, button7, button8, button9, user_symbol, compSymbol, game, skin_user_X, skin_user_Zero, skin_comp_Zero, skin_comp_X
    cursor.execute("SELECT lang FROM game WHERE id = ?", (callback.from_user.id,))
    lang = cursor.fetchone()[0]
    win = 0
    if (
    (button1.text == user_symbol and button2.text == user_symbol and button3.text == user_symbol) or
    (button4.text == user_symbol and button5.text == user_symbol and button6.text == user_symbol) or
    (button7.text == user_symbol and button8.text == user_symbol and button9.text == user_symbol) or
    
    (button1.text == user_symbol and button4.text == user_symbol and button7.text == user_symbol) or
    (button2.text == user_symbol and button5.text == user_symbol and button8.text == user_symbol) or 
    (button3.text == user_symbol and button6.text == user_symbol and button9.text == user_symbol) or
    
    (button1.text == user_symbol and button5.text == user_symbol and button9.text == user_symbol) or
    (button7.text == user_symbol and button5.text == user_symbol and button3.text == user_symbol)):
        await callback.message.edit_text(i18n.get("win_text"), reply_markup=keyboard_ttt)
        win = 1
        
        cursor.execute("SELECT x2_score FROM game WHERE id = ?", (callback.from_user.id,))
        x2_score = cursor.fetchone()[0]
        
        cursor.execute("SELECT score FROM game WHERE id = ?", (callback.from_user.id,))
        score = cursor.fetchone()[0]
        
        cursor.execute("UPDATE game SET score = ? WHERE id = ?", (score + (1 * x2_score), callback.from_user.id,))
        conn.commit()
    elif (
    (button1.text == compSymbol and button2.text == compSymbol and button3.text == compSymbol) or
    (button4.text == compSymbol and button5.text == compSymbol and button6.text == compSymbol) or
    (button7.text == compSymbol and button8.text == compSymbol and button9.text == compSymbol) or

    (button1.text == compSymbol and button4.text == compSymbol and button7.text == compSymbol) or
    (button2.text == compSymbol and button5.text == compSymbol and button8.text == compSymbol) or 
    (button3.text == compSymbol and button6.text == compSymbol and button9.text == compSymbol) or

    (button1.text == compSymbol and button5.text == compSymbol and button9.text == compSymbol) or
    (button7.text == compSymbol and button5.text == compSymbol and button3.text == compSymbol)):
        await callback.message.edit_text(i18n.get("lose_text"), reply_markup=keyboard_ttt)
        win = 2
    else:
        win = 3
        
    game = 0

        
    return win
                
