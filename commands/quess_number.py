from aiogram import F, Router
from random import randint
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_i18n import I18nContext
from database import *

router_guess_number = Router()

is_game = True  

@router_guess_number.message(Command("guess_number"))
async def play_guess_number(message: Message, i18n:I18nContext):
	global is_game, secret_number
	is_game = True

	cursor.execute("SELECT lang FROM game WHERE id = ?", (message.from_user.id,))
	lang = cursor.fetchone()[0]

	name = message.from_user.mention_html()
 
	secret_number = randint(1, 100)
	await message.answer(i18n.get("guess_number_start_text", user=name), parse_mode="html")

	await message.answer_dice(emoji="🎲")
	await message.answer(i18n.get(f"text_after_guess_number_start_text"))
  
	cursor.execute("SELECT x2_score FROM game WHERE id = ?", (message.from_user.id,))
	x2_score = cursor.fetchone()[0]
 
	cursor.execute("SELECT answer FROM game WHERE id = ?", (message.from_user.id,))
	answer = cursor.fetchone()[0]
 
	if answer >= 1:
		await message.answer(i18n.get(f"answer", secret_number=secret_number), parse_mode="html")
		cursor.execute("UPDATE game SET answer = ? WHERE id = ?", (answer - 1, message.from_user.id,))
		conn.commit()
	

	@router_guess_number.message(lambda message: is_game)
	async def on_game(message: Message, i18n:I18nContext):
		cursor.execute("SELECT lang FROM game WHERE id = ?", (message.from_user.id,))
		lang = cursor.fetchone()[0]
		try:
			text = int(message.text)
			if text == secret_number:
				cursor.execute("SELECT score FROM game WHERE id = ?", (message.from_user.id,))
				score = cursor.fetchone()[0]
				await message.answer(i18n.get("text_win_guess_number"))
				cursor.execute("UPDATE game SET score = ? WHERE id = ?", (score + (1 * x2_score), message.from_user.id,))
				conn.commit()
    
				global is_game
				is_game = False
			elif text > secret_number:
				await message.answer(i18n.get("number_is_more"))
			else:
				await message.answer(i18n.get("number_is_less"))
		except ValueError:
			await message.answer(i18n.get("enter_a_number"))


@router_guess_number.message(Command("stop"))
async def stop_game(message: Message, i18n:I18nContext):
	cursor.execute("SELECT lang FROM game WHERE id = ?", (message.from_user.id,))
	lang = cursor.fetchone()[0]
	await message.answer(i18n.get("game_is_over"))
	global is_game
	is_game = False