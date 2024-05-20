from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton as ikb
from aiogram.types import InlineKeyboardMarkup as ikm
from database import *
from aiogram.filters import Command
from aiogram_i18n import I18nContext, LazyProxy
from aiogram_i18n.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)  

router_shop = Router()
 
is_shop = True

nl = "\n"

@router_shop.message(Command("shop"))
async def shop(message: Message, i18n: I18nContext):
	global is_shop
	is_shop = True
	cursor.execute("SELECT score FROM game WHERE id = ?", (message.from_user.id,))
	score = cursor.fetchone()[0]
	cursor.execute("SELECT answer FROM game WHERE id = ?", (message.from_user.id,))
	answer = cursor.fetchone()[0]
	cursor.execute("SELECT premium_stars FROM game WHERE id = ?", (message.from_user.id,))
	premium_stars = cursor.fetchone()[0]

	button_one = ikb(text="1", callback_data="one")
	button_two = ikb(text="2", callback_data="two")
	button_three = ikb(text="3", callback_data="three")

	keyboard_shop = ikm(inline_keyboard=[
		[button_one, button_two, button_three]
	])

	nl = "\n"

	await message.answer(i18n.get("shop_message", score=score, answer=answer, nl=nl, premium_stars=premium_stars), parse_mode="html", reply_markup=keyboard_shop)

	@router_shop.callback_query(F.data == "one")
	async def one_callback(callback: CallbackQuery, i18n: I18nContext):
		cursor.execute("SELECT score FROM game WHERE id = ?", (callback.from_user.id,))
		score = cursor.fetchone()[0]
		if score >= 4:
			cursor.execute("SELECT answer FROM game WHERE id = ?", (callback.from_user.id,))
			answer = cursor.fetchone()[0]
			cursor.execute("UPDATE game SET answer = ? WHERE id = ?", (answer + 1, callback.from_user.id,))
			conn.commit()
			cursor.execute("UPDATE game SET score = ? WHERE id = ?", (score - 4, callback.from_user.id,))
			conn.commit()
			nl = "\n"
			await callback.message.answer(i18n.get("purchase_completed", score=score, nl=nl))

		else:
			cursor.execute("SELECT answer FROM game WHERE id = ?", (callback.from_user.id,))
			answer = cursor.fetchone()[0]
			cursor.execute("SELECT score FROM game WHERE id = ?", (callback.from_user.id,))
			score = cursor.fetchone()[0]
			await callback.message.answer(i18n.get("check_the_balance"))

	@router_shop.callback_query(F.data == "two")
	async def two_callback(callback: CallbackQuery, i18n: I18nContext):
		nl = "\n"
		cursor.execute("SELECT score FROM game WHERE id = ?", (callback.from_user.id,))
		score = cursor.fetchone()[0]
		cursor.execute("SELECT premium FROM game WHERE id = ?", (message.from_user.id,))
		premium = cursor.fetchone()[0]
		cursor.execute("SELECT x2_score FROM game WHERE id = ?", (callback.from_user.id,))
		x2_score = cursor.fetchone()[0]
		if x2_score >= 2:
			await callback.message.answer(i18n.get("you_already_bought_it"))
		else:
			if score >= 100:
				if premium == 0:
					add = 2
				else:
					add = 4
				cursor.execute("UPDATE game SET x2_score = ? WHERE id = ?", (add, callback.from_user.id,))
				conn.commit()
				cursor.execute("UPDATE game SET score = ? WHERE id = ?", (score - 100, callback.from_user.id,))
				conn.commit()
				cursor.execute("SELECT score FROM game WHERE id = ?", (callback.from_user.id,))
				score = cursor.fetchone()[0]
				nl = "\n"
				await callback.message.answer(i18n.get("purchase_completed", score=score, nl=nl))
			else:
				await callback.message.answer(i18n.get("check_the_balance"))

	@router_shop.callback_query(F.data == "three")
	async def three_callback(callback: CallbackQuery, i18n: I18nContext):
		button_basketball = InlineKeyboardButton(text=LazyProxy("basketball_ball"), callback_data="basketball_ball")
		button_soccer = InlineKeyboardButton(text=LazyProxy("soccer_ball"), callback_data="soccer_ball")
		button_volleyball = InlineKeyboardButton(text=LazyProxy("volleyball_ball"), callback_data="volleyball_ball")
		button_football = InlineKeyboardButton(text=LazyProxy("football_ball"), callback_data="football_ball")
		button_fire = InlineKeyboardButton(text=LazyProxy("fire"), callback_data="fire")
		button_note = InlineKeyboardButton(text=LazyProxy("note"), callback_data="note")
		button_snow = InlineKeyboardButton(text=LazyProxy("snow"), callback_data="snow")
		button_sword = InlineKeyboardButton(text=LazyProxy("sword"), callback_data="sword")

		button_fire_heart = InlineKeyboardButton(text=LazyProxy("fire_heart"), callback_data="fire_heart")
		button_purple_heart = InlineKeyboardButton(text=LazyProxy("purple_heart"), callback_data="purple_heart")
		button_table_tennis = InlineKeyboardButton(text=LazyProxy("table_tennis"), callback_data="table_tennis")
		button_trophy = InlineKeyboardButton(text=LazyProxy("trophy"), callback_data="trophy")
		button_poo = InlineKeyboardButton(text=LazyProxy("poo"), callback_data="poo")
		button_premium_star = InlineKeyboardButton(text=LazyProxy("premium_star"), callback_data="premium_star")
		button_star = InlineKeyboardButton(text=LazyProxy("star"), callback_data="star")
		button_back = InlineKeyboardButton(text=LazyProxy("back"), callback_data="back_shop")


		cursor.execute("SELECT premium FROM game WHERE id = ?", (message.from_user.id,))
		premium = cursor.fetchone()[0]

		if premium == 0:
			keyboard_skins = InlineKeyboardMarkup(inline_keyboard=[
				[button_basketball],
				[button_football],
				[button_note],
				[button_sword],
				[button_back]
			])
		else:
			keyboard_skins = InlineKeyboardMarkup(inline_keyboard=[
				[button_basketball],
				[button_soccer],
				[button_volleyball],
				[button_football],
				[button_table_tennis],
				[button_fire],
				[button_fire_heart],
				[button_purple_heart],
				[button_star],
				[button_premium_star],
				[button_note],
				[button_snow],
				[button_sword],
				[button_poo],
				[button_trophy],
				[button_back]
			])

		await callback.message.edit_text(i18n.get("choose_a_skin"), reply_markup=keyboard_skins)

		@router_shop.callback_query(F.data == "back_shop")
		async def back_func(callback: CallbackQuery):
			nl = "\n"
			await callback.message.edit_text(i18n.get("shop_message", score=score, answer=answer, nl=nl, premium_stars=premium_stars), parse_mode="html", reply_markup=keyboard_shop)

		list = [("basketball_ball"), ("soccer_ball"), 
		  ("volleyball_ball"), ("football_ball"), 
		  ("fire"), ("note"), 
		  ("snow"), ("sword"), 
		  ("premium_star"), ("star"),
		  ("table_tennis"), ("poo"),
		  ("trophy"), ("purple_heart"),
		  ("fire_heart")]
		for callback_data in list:
			@router_shop.callback_query(F.data == callback_data)
			async def set_skin(callback: CallbackQuery, name=callback_data):
				if premium == 0:
					emoji = "⭐"
					cursor.execute("SELECT score FROM game WHERE id = ?", (message.from_user.id,))
					score = cursor.fetchone()[0]
					cursor.execute(f"SELECT {name}_skin FROM skins WHERE id = ?", (message.from_user.id,))
					name_skin = cursor.fetchone()[0]
					if name_skin == 1:
						await callback.message.edit_text(i18n.get("you_have_skin"))
					else:
						if score >= 50:
							cursor.execute(f"UPDATE skins SET {name}_skin = ? WHERE id = ?", (1, callback.from_user.id,))
							conn.commit()
							cursor.execute("UPDATE game SET score = ? WHERE id = ?", (score - 50, callback.from_user.id,))
							conn.commit()
							cursor.execute("SELECT score FROM game WHERE id = ?", (message.from_user.id,))
							score = cursor.fetchone()[0]
							nl = "\n"
							await callback.message.edit_text(i18n.get("skin_selected", score=score, nl=nl, sale=50))
						else:
							cursor.execute("SELECT score FROM game WHERE id = ?", (message.from_user.id,))
							score = cursor.fetchone()[0]
							nl = "\n"
							await callback.message.edit_text(i18n.get("not_enough_stars_shop", nl=nl, score=score))
				else:
					cursor.execute("SELECT score FROM game WHERE id = ?", (message.from_user.id,))
					score = cursor.fetchone()[0]
					cursor.execute("SELECT premium_stars FROM game WHERE id = ?", (message.from_user.id,))
					premium_stars = cursor.fetchone()[0]
					cursor.execute(f"SELECT {name}_skin FROM skins WHERE id = ?", (message.from_user.id,))
					name_skin = cursor.fetchone()[0]
					if name_skin == 1:
						await callback.message.edit_text(i18n.get("you_have_skin"))
					else:
						emoji = "⭐"
						if score >= 50 or premium_stars >= 5:
							cursor.execute("SELECT premium_stars FROM game WHERE id = ?", (message.from_user.id,))
							premium_stars = cursor.fetchone()[0]
							cursor.execute(f"UPDATE skins SET {name}_skin = ? WHERE id = ?", (1, callback.from_user.id,))
							conn.commit()
							cursor.execute("UPDATE game SET premium_stars = ? WHERE id = ?", (premium_stars - 5, callback.from_user.id,))
							conn.commit()
							cursor.execute("SELECT premium_stars FROM game WHERE id = ?", (message.from_user.id,))
							premium_stars = cursor.fetchone()[0]
							nl = "\n"
							await callback.message.edit_text(i18n.get("skin_selected", score=premium_stars, nl=nl, sale=5, emoji=emoji))
						else:
							cursor.execute("SELECT premium_stars FROM game WHERE id = ?", (message.from_user.id,))
							premium_stars = cursor.fetchone()[0]
							nl = "\n"
							await callback.message.edit_text(i18n.get("not_enough_stars_shop", nl=nl, score=premium_stars, emoji=emoji))
