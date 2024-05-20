from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n.types import InlineKeyboardButton
from aiogram_i18n import I18nContext, LazyProxy
from database import *

    
router_change_skin = Router()

@router_change_skin.message(Command("change_skin"))
async def change_skin_func(message: Message, i18n: I18nContext):
    cursor.execute("SELECT lang FROM game WHERE id = ?", (message.from_user.id,))
    lang = cursor.fetchone()[0]
    builder = InlineKeyboardBuilder()

    button_standart = InlineKeyboardButton(text=LazyProxy("standart"), callback_data="standart_change_skin")

    builder.add(button_standart)

    list_skins = [(i18n.get("basketball_ball"), "basketball_ball_change_skin"),
                (i18n.get("soccer_ball"), "soccer_ball_change_skin"),
                (i18n.get("volleyball_ball"), "volleyball_ball_change_skin"),
                (i18n.get("football_ball"), "football_ball_change_skin"),
                (i18n.get("fire"), "fire_change_skin"),
                (i18n.get("note"), "note_change_skin"),
                (i18n.get("snow"), "snow_change_skin"),
                (i18n.get("sword"), "sword_change_skin"),
                (i18n.get("fire_heart"), "fire_heart_change_skin"),
                (i18n.get("purple_heart"), "purple_heart_change_skin"),
                (i18n.get("table_tennis"), "table_tennis_change_skin"),
                (i18n.get("trophy"), "trophy_change_skin"),
                (i18n.get("poo"), "poo_change_skin"),
                (i18n.get("premium_star"), "premium_star_change_skin"),
                (i18n.get("star"), "star_change_skin")]

    for text, callback_data in list_skins:
        parts = callback_data.split("_change_skin")
        name = parts[0]
        cursor.execute(f"SELECT {name}_skin FROM skins WHERE id = ?", (message.from_user.id,))
        name_skin = cursor.fetchone()[0]
        if name_skin == 1:
            builder.button(text=text, callback_data=callback_data)
        else:
            pass
        
    builder.adjust(1, 1)

    await message.answer(i18n.get("choose_a_skin_for_ttt"), reply_markup=builder.as_markup())

    list = [("standart_change_skin"), 
            ("basketball_ball_change_skin"), 
            ("soccer_ball_change_skin"), 
            ("volleyball_ball_change_skin"), 
            ("football_ball_change_skin"), 
            ("fire_change_skin"), 
            ("note_change_skin"), ("snow_change_skin"), ("sword_change_skin"),
            ("fire_heart_change_skin"),
            ("purple_heart_change_skin"),
            ("table_tennis_change_skin"),
            ("trophy_change_skin"),
            ("poo_change_skin"),
            ("premium_star_change_skin"),
            ("star_change_skin")]
    for callback_data in list:
        @router_change_skin.callback_query(F.data == callback_data)
        async def change_skin(callback: CallbackQuery, i18n: I18nContext, name=callback_data):
            parts = name.split("_change_skin")
            name = parts[0]
            cursor.execute(f"UPDATE game SET skin = ? WHERE id = ?", (name, callback.from_user.id,))
            conn.commit()
            await callback.message.edit_text(i18n.get("skin_selected_change"), parse_mode="html")

    