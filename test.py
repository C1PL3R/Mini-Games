from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import F, Router, enums
import asyncio
import random
from aiogram import Bot, F
from aiogram.filters import Command
from database import *

router_test = Router()

TOKEN = "5957173294:AAEIgZLBSCXfZM9mfPTayI8KygPFiYQXL5Q"
bot = Bot(token=TOKEN)

button_1_online = InlineKeyboardButton(text="  ", callback_data=f"button_1_online")
button_2_online = InlineKeyboardButton(text="  ", callback_data=f"button_2_online")
button_3_online = InlineKeyboardButton(text="  ", callback_data=f"button_3_online")
                                      
button_4_online = InlineKeyboardButton(text="  ", callback_data=f"button_4_online")
button_5_online = InlineKeyboardButton(text="  ", callback_data=f"button_5_online")
button_6_online = InlineKeyboardButton(text="  ", callback_data=f"button_6_online")
                                      
button_7_online = InlineKeyboardButton(text="  ", callback_data=f"button_7_online")
button_8_online = InlineKeyboardButton(text="  ", callback_data=f"button_8_online")
button_9_online = InlineKeyboardButton(text="  ", callback_data=f"button_9_online")
                                      
                                                             
keyboard_ttt_online = InlineKeyboardMarkup(inline_keyboard=[
    [button_1_online, button_2_online, button_3_online],
    [button_4_online, button_5_online, button_6_online],
    [button_7_online, button_8_online, button_9_online],
])

attemps = 1

user_id = 0

my_message = 0
opponent_message = 0
opponents_ids = []

members_game = []
opponent_id_list = []

select_mess_dict = {}

skin_p1_Zero = "⭕"
skin_p1_X = "❌"

skin_p2_Zero = "⭕"
skin_p2_X = "❌"

player_1_symbol = ""
player_2_symbol = ""

button_yes_status = True
while_status = 1

my_id = 0
opponent_id = 0
text = ""
mess = 0


@router_test.message(Command('tictactoe_online'))#треба зробити так щоб кнопки підтвердження зникали завжди після нажаття
async def tictactoe(message: Message, members_game=members_game):
    global opponent_message, while_status, opponent_id, my_id, my_message, mess, button_yes_status, select_mess_dict
    select_mess_dict = {opponent_id: [], my_id: []}
    a = 0
    a += 1
    while_status = 1
    opponents_ids = []
    
    opponent_id_list = []
    members_game = []

    opponent_mess = 0
    # player_1_symbol = ""
    # player_2_symbol = ""

    cursor.execute("UPDATE online SET online = 1 WHERE id = ?", (message.from_user.id,))
    conn.commit()

    

    time = 0

    my_message = await bot.send_message(chat_id=message.from_user.id, text="Зараз підбираються гравці!")
    game_status = True
    if while_status == 1:
        while True:
            cursor.execute("SELECT online, id FROM online WHERE online = 1")
            online_while = cursor.fetchall()
            
            if len(online_while) > 1:
                await my_message.edit_text(text=f"Час очікування: {time} с.")
                time = 0
                while_status = 0
                break
            else:
                await bot.send_chat_action(action=enums.ChatAction.CHOOSE_STICKER, chat_id=message.chat.id)
                await asyncio.sleep(1)
                time += 1
                my_message = await my_message.edit_text(text=f"Зараз підбираються гравці! Час очікування: {time} с.")
                
            if time == 30:
                my_message = await my_message.edit_text(text=f"Спробуйте пізніше 😉!")
                while_status = 0
                break
    else:
        pass

    cursor.execute("SELECT online, id FROM online WHERE online = 1")
    idsOpponentsList = cursor.fetchall()

    opponents_ids = []

    for online, user_id in idsOpponentsList:
        if user_id != message.from_user.id:
            opponents_ids.append(user_id)
        if user_id == message.from_user.id:
            my_id = user_id

    if opponents_ids:
        opponent_id = random.choice(opponents_ids)
        members_game = [opponent_id, my_id]
    else:
        members_game = []

    cursor.execute("UPDATE online SET opponent_id = ? WHERE id = ?", (opponent_id, my_id,))
    conn.commit()
    cursor.execute("UPDATE online SET my_id = ? WHERE id = ?", (my_id, my_id,))
    conn.commit()
    cursor.execute("UPDATE online SET opponent_id = ? WHERE id = ?", (opponent_id, opponent_id,))
    conn.commit()
    cursor.execute("UPDATE online SET my_id = ? WHERE id = ?", (my_id, opponent_id,))
    conn.commit()

    cursor.execute("SELECT opponent_id FROM online WHERE id = ?", (my_id,))
    opponent_id = cursor.fetchone()[0]
    cursor.execute("SELECT my_id FROM online WHERE id = ?", (my_id,))
    my_id = cursor.fetchone()[0]

    members_game = [opponent_id, my_id]

    select_mess_dict = {}

    button_yes = InlineKeyboardButton(text="✅ Так ✅", callback_data=f"button_yes_test")
    button_no = InlineKeyboardButton(text="❌ Ні ❌", callback_data=f"button_no_test")
                            
    keyboard_choice = InlineKeyboardMarkup(inline_keyboard=[
        [button_yes, button_no]
    ])

    select_mess_dict = {opponent_id: [], my_id: []}  # Ініціалізуємо словник з порожніми списками

    for id in members_game:
        select = await bot.send_message(chat_id=id, text=f"Супериник вже знайдений, грати?", parse_mode="html", reply_markup=keyboard_choice)
        select_mess_dict[id].append(select)

        await bot.delete_message(chat_id=int(id), message_id=select[0].message_id)
        select.pop(0)


@router_test.callback_query(F.data == "button_no_test")
async def callback_query_button_no(callback: CallbackQuery):  
    global opponent_id, my_id, select_mess_dict

    cursor.execute("SELECT online FROM online WHERE id = ?", (opponent_id,))
    online_opponent = cursor.fetchone()[0]
    cursor.execute("SELECT online FROM online WHERE id = ?", (my_id,))
    online_my = cursor.fetchone()[0]
    if online_opponent == 1 or online_my == 1:
        list_ids = [opponent_id, my_id]

        for user_id in list_ids:
            try:
                message_id = select_mess_dict.get(user_id)
                await bot.delete_message(chat_id=user_id, message_id=message_id[0].message_id)
            except Exception:
                pass
        global members_game, opponent_message, my_message
        cursor.execute("UPDATE online SET online = 0 WHERE id = ?", (opponent_id,))
        conn.commit()
        cursor.execute("UPDATE online SET online = 0 WHERE id = ?", (my_id,))
        conn.commit()

        
        await bot.send_message(chat_id=opponent_id, text="Гру закінчено!")
        await bot.send_message(chat_id=my_id, text="Гру закінчено!")

        members_game = []
    else:
        await bot.send_message(chat_id=callback.from_user.id, text="Гру закічено")
    
        

@router_test.callback_query(F.data == "button_yes_test")#треба зробити так щоб кнопки підтвердження зникали завжди після нажаття
async def callback_query_button_yes(callback: CallbackQuery, bot: Bot, 
                                    button_1_online=button_1_online, 
                                    button_2_online=button_2_online, button_3_online=button_3_online, 
                                    button_4_online=button_4_online, button_5_online=button_5_online, 
                                    button_6_online=button_6_online, button_7_online=button_7_online, 
                                    button_8_online=button_8_online, button_9_online=button_9_online, 
                                    opponent_message=opponent_message):
    global skin_p2_X, skin_p1_X, skin_p1_Zero, skin_p2_Zero, opponent_id, my_id, my_message, mess, button_yes_status, select_mess_dict

    list_ids = [opponent_id, my_id]

    for user_id in list_ids:
        try:
            message_id = select_mess_dict.get(user_id)
            await bot.delete_message(chat_id=user_id, message_id=message_id[0].message_id)
        except Exception:
            pass
        
    
    list_ids = [opponent_id, my_id]
    for id in list_ids:
        cursor.execute("UPDATE online SET online = 0 WHERE id = ?", (id,))
        conn.commit()

    cursor.execute("SELECT skin FROM game WHERE id = ?", (my_id,))
    my_skin = cursor.fetchone()[0]  

    cursor.execute("SELECT skin FROM game WHERE id = ?", (opponent_id,))
    opponent_skin = cursor.fetchone()[0]  


    if my_skin == "standart": 
        skin_p1_X = "❌"
        skin_p1_Zero = "⭕"
    elif my_skin == "basketball_ball":
        skin_p1_X = "🏀"
        skin_p1_Zero = "🟠"
    elif my_skin == "soccer_ball":
        skin_p1_X = "⚽"
        skin_p1_Zero = "⚪"
    elif my_skin == "volleyball_ball":
        skin_p1_X = "🏐"
        skin_p1_Zero = "⚪"
    elif my_skin == "football_ball":
        skin_p1_X = "🏈"
        skin_p1_Zero = "🟤"
    elif my_skin == "fire":
        skin_p1_X = "🔥"
        skin_p1_Zero = "🟠"
    elif my_skin == "note":
        skin_p1_X = "🎵"
        skin_p1_Zero = "⚫"
    elif my_skin == "snow":
        skin_p1_X = "❄️"
        skin_p1_Zero = "🔵"
    elif my_skin == "sword":
        skin_p1_X = "⚔️"
        skin_p1_Zero = "🔘"
    elif my_skin == "fire_heart":
        skin_p1_X = "❤️‍🔥"
        skin_p1_Zero = "🔴"
    elif my_skin == "purple_heart":
        skin_p1_X = "💖"
        skin_p1_Zero = "🟣"
    elif my_skin == "table_tennis":
        skin_p1_X = "🏓"
        skin_p1_Zero = "🔴"
    elif my_skin == "trophy":
        skin_p1_X = "🏆"
        skin_p1_Zero = "🌕"
    elif my_skin == "poo":
        skin_p1_X = "💩"
        skin_p1_Zero = "🟤"
    elif my_skin == "star":
        skin_p1_X = "⭐️"
        skin_p1_Zero = "🌝"
    elif my_skin == "premium_star":
        skin_p1_X = "🌟"
        skin_p1_Zero = "🤩"

    if opponent_skin == "standart": 
        skin_p2_X = "❌"
        skin_p2_Zero = "⭕"
    elif opponent_skin == "basketball_ball":
        skin_p2_X = "🏀"
        skin_p2_Zero = "🟠"
    elif opponent_skin == "soccer_ball":
        skin_p2_X = "⚽"
        skin_p2_Zero = "⚪"
    elif opponent_skin == "volleyball_ball":
        skin_p2_X = "🏐"
        skin_p2_Zero = "⚪"
    elif opponent_skin == "football_ball":
        skin_p2_X = "🏈"
        skin_p2_Zero = "🟤"
    elif opponent_skin == "fire":
        skin_p2_X = "🔥"
        skin_p2_Zero = "🟠"
    elif opponent_skin == "note":
        skin_p2_X = "🎵"
        skin_p2_Zero = "⚫"
    elif opponent_skin == "snow":
        skin_p2_X = "❄️"
        skin_p2_Zero = "🔵"
    elif opponent_skin == "sword":
        skin_p2_X = "⚔️"
        skin_p2_Zero = "🔘"
    elif opponent_skin == "fire_heart":
        skin_p2_X = "❤️‍🔥"
        skin_p2_Zero = "🔴"
    elif opponent_skin == "purple_heart":
        skin_p2_X = "💖"
        skin_p2_Zero = "🟣"
    elif opponent_skin == "table_tennis":
        skin_p2_X = "🏓"
        skin_p2_Zero = "🔴"
    elif opponent_skin == "trophy":
        skin_p2_X = "🏆"
        skin_p2_Zero = "🌕"
    elif opponent_skin == "poo":
        skin_p2_X = "💩"
        skin_p2_Zero = "🟤"
    elif opponent_skin == "star":
        skin_p2_X = "⭐️"
        skin_p2_Zero = "🌝"
    elif opponent_skin == "premium_star":
        skin_p2_X = "🌟"
        skin_p2_Zero = "🤩"


    attemps = 1

    buttons_list = [(button_1_online), (button_2_online), (button_3_online), 
                    (button_4_online), (button_5_online), (button_6_online), 
                    (button_7_online), (button_8_online), (button_9_online)]
    
    for btn in buttons_list:
        btn.text = "  "

    game_mess_dict = {}
    select_mess_dict = {}

    list_ids = [opponent_id, my_id]
    for id in list_ids:
        if id == my_id:
            buttonX = InlineKeyboardButton(text=skin_p1_X, callback_data="cross_online")
            buttonZero = InlineKeyboardButton(text=skin_p1_Zero, callback_data="zero_online")
        else:
            buttonX = InlineKeyboardButton(text=skin_p2_X, callback_data="cross_online")
            buttonZero = InlineKeyboardButton(text=skin_p2_Zero, callback_data="zero_online")
        
        keyboardXandZero_online = InlineKeyboardMarkup(inline_keyboard=[
            [buttonX, buttonZero]
        ])

        select = await bot.send_message(chat_id=id, text="Виберіть ким ви будете:", parse_mode="html", reply_markup=keyboardXandZero_online)
        select_mess_dict[id] = select


    @router_test.callback_query(F.data == "cross_online")
    async def callback_cross(callback: CallbackQuery, skin_p1_X=skin_p1_X, skin_p2_Zero=skin_p2_Zero, game_mess_dict=game_mess_dict):
        global player_1_symbol, player_2_symbol
        if my_skin == opponent_skin:
            player_1_symbol = skin_p1_X
            player_2_symbol = skin_p2_Zero
        else:
            player_1_symbol = skin_p1_X
            player_2_symbol = skin_p2_X
        game = 1
        
        list_ids = [opponent_id, my_id]
        for id in list_ids:
            game_mess = await bot.send_message(chat_id=id, text="Гра Хрестики-нолики", parse_mode="html", reply_markup=keyboard_ttt_online)
            game_mess_dict[id] = game_mess

        for id in list_ids:
            select = select_mess_dict.get(id)
            await bot.edit_message_text(chat_id=id, message_id=select.message_id, text="Виберіть ким ви будете:")

    @router_test.callback_query(F.data == "zero_online")
    async def callback_zero(callback: CallbackQuery, skin_p1_X=skin_p1_X, skin_p2_Zero=skin_p2_Zero, game_mess_dict=game_mess_dict):
        global player_1_symbol, player_2_symbol
        if my_skin == opponent_skin:
            player_2_symbol = skin_p2_Zero
            player_1_symbol = skin_p1_X
        else:
            player_2_symbol = skin_p2_Zero
            player_1_symbol = skin_p1_Zero

        game = 1
        
        list_ids = [opponent_id, my_id]
        for id in list_ids:
            game_mess = await bot.send_message(chat_id=id, text="Гра Хрестики-нолики", parse_mode="html", reply_markup=keyboard_ttt_online)
            game_mess_dict[id] = game_mess


        for id in list_ids:
            select = select_mess_dict.get(id)
            await bot.edit_message_text(chat_id=id, message_id=select.message_id, text="Виберіть ким ви будете:")

    btn_list = [
        (button_1_online, "button_1_online"),
        (button_2_online, "button_2_online"),
        (button_3_online, "button_3_online"),
        (button_4_online, "button_4_online"),
        (button_5_online, "button_5_online"),
        (button_6_online, "button_6_online"),
        (button_7_online, "button_7_online"),
        (button_8_online, "button_8_online"),
        (button_9_online, "button_9_online")
    ]

    for btn, btn_callback in btn_list:
        @router_test.callback_query(F.data == btn_callback)
        async def callback_ttt_game(callback: CallbackQuery, bot: Bot, opponent_id=opponent_id, my_id=my_id, btn=btn, game_mess_dict=game_mess_dict):
            global player_1_symbol, player_2_symbol, attemps, text

            if callback.from_user.id == my_id:
                emoji = player_1_symbol
            if callback.from_user.id == opponent_id:
                emoji = player_2_symbol

            

            if btn.text == "  ":
                if attemps == 1 and callback.from_user.id == my_id:
                    btn.text = emoji
                    attemps = 0
                    text = "Хрестики-нолики"
                if attemps == 0 and callback.from_user.id == opponent_id:
                    btn.text = emoji
                    attemps = 1
                    text = "Гра Хрестики-нолики!"
            else:
                text = "Ця клітинка зайнята!"
                game_mess = game_mess_dict.get(callback.from_user.id)
                await bot.edit_message_text(chat_id=callback.from_user.id, message_id=game_mess.message_id, text=text, reply_markup=keyboard_ttt_online)

            
            list_ids = [opponent_id, my_id]
            for id in list_ids:
                game_mess = game_mess_dict.get(id)
                
                await bot.edit_message_text(chat_id=id, message_id=game_mess.message_id, text=text, reply_markup=keyboard_ttt_online)

            win = 0
            if (
            (button_1_online.text == player_1_symbol and button_2_online.text == player_1_symbol and button_3_online.text == player_1_symbol) or
            (button_4_online.text == player_1_symbol and button_5_online.text == player_1_symbol and button_6_online.text == player_1_symbol) or
            (button_7_online.text == player_1_symbol and button_8_online.text == player_1_symbol and button_9_online.text == player_1_symbol) or
            
            (button_1_online.text == player_1_symbol and button_4_online.text == player_1_symbol and button_7_online.text == player_1_symbol) or
            (button_2_online.text == player_1_symbol and button_5_online.text == player_1_symbol and button_8_online.text == player_1_symbol) or 
            (button_3_online.text == player_1_symbol and button_6_online.text == player_1_symbol and button_9_online.text == player_1_symbol) or
            
            (button_1_online.text == player_1_symbol and button_5_online.text == player_1_symbol and button_9_online.text == player_1_symbol) or
            (button_7_online.text == player_1_symbol and button_5_online.text == player_1_symbol and button_3_online.text == player_1_symbol)):
                list_ids = [opponent_id, my_id]
                for id in list_ids:
                    if id == my_id:
                        game_mess = game_mess_dict.get(id)
                        await bot.edit_message_text(chat_id=id, message_id=game_mess.message_id, text="Ви виграли!")
                    else:
                        game_mess = game_mess_dict.get(id)
                        await bot.edit_message_text(chat_id=id, message_id=game_mess.message_id, text="Ви програли!")

                win = 1
                
                cursor.execute("SELECT x2_score FROM game WHERE id = ?", (my_id,))
                x2_score = cursor.fetchone()[0]
                
                cursor.execute("SELECT score FROM game WHERE id = ?", (my_id,))
                score = cursor.fetchone()[0]
                
                cursor.execute("UPDATE game SET score = ? WHERE id = ?", (score + (1 * x2_score), my_id,))
                conn.commit()
            elif (
            (button_1_online.text == player_2_symbol and button_2_online.text == player_2_symbol and button_3_online.text == player_2_symbol) or
            (button_4_online.text == player_2_symbol and button_5_online.text == player_2_symbol and button_6_online.text == player_2_symbol) or
            (button_7_online.text == player_2_symbol and button_8_online.text == player_2_symbol and button_9_online.text == player_2_symbol) or

            (button_1_online.text == player_2_symbol and button_4_online.text == player_2_symbol and button_7_online.text == player_2_symbol) or
            (button_2_online.text == player_2_symbol and button_5_online.text == player_2_symbol and button_8_online.text == player_2_symbol) or 
            (button_3_online.text == player_2_symbol and button_6_online.text == player_2_symbol and button_9_online.text == player_2_symbol) or

            (button_1_online.text == player_2_symbol and button_5_online.text == player_2_symbol and button_9_online.text == player_2_symbol) or
            (button_7_online.text == player_2_symbol and button_5_online.text == player_2_symbol and button_3_online.text == player_2_symbol)):
                list_ids = [opponent_id, my_id]
                for id in list_ids:
                    if id == opponent_id:
                        game_mess = game_mess_dict.get(id)
                        await bot.edit_message_text(chat_id=id, message_id=game_mess.message_id, text="Ви виграли!")
                    else:
                        game_mess = game_mess_dict.get(id)
                        await bot.edit_message_text(chat_id=id, message_id=game_mess.message_id, text="Ви програли!")

                cursor.execute("SELECT x2_score FROM game WHERE id = ?", (opponent_id,))
                x2_score = cursor.fetchone()[0]
                
                cursor.execute("SELECT score FROM game WHERE id = ?", (opponent_id,))
                score = cursor.fetchone()[0]
                
                cursor.execute("UPDATE game SET score = ? WHERE id = ?", (score + (1 * x2_score), opponent_id,))
                conn.commit()
                win = 2
         
