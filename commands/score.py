from aiogram import F, Router
from aiogram.types import Message
from database import *
from aiogram_i18n import I18nContext
from aiogram.filters import Command
from aiogram import Bot

TOKEN = "5957173294:AAEIgZLBSCXfZM9mfPTayI8KygPFiYQXL5Q"
bot = Bot(token=TOKEN)

router_score = Router()

@router_score.message(Command("score"))
async def close(message: Message, i18n: I18nContext):
	
	cursor.execute("SELECT score FROM game WHERE id = ?", (message.from_user.id,))
	score = cursor.fetchone()[0]
	cursor.execute("SELECT x2_score FROM game WHERE id = ?", (message.from_user.id,))
	x2_score = cursor.fetchone()[0]
	if x2_score == 1:
		text = i18n.get("not_bought")
	else:
		text = i18n.get("bought")

	nl = "\n"
	await message.answer(i18n.get("score_text", score=score, text=text, nl=nl))


@router_score.message(Command("stars"))
async def close(message: Message, i18n: I18nContext):
	cursor.execute("SELECT premium FROM game WHERE id = ?", (message.from_user.id,))
	premium = cursor.fetchone()[0]
	if premium == 0:
		await message.answer(i18n.get("not_premium_account"))
	else:
		cursor.execute("SELECT premium_stars FROM game WHERE id = ?", (message.from_user.id,))
		premium_stars = cursor.fetchone()[0]
		nl = "\n"
		await message.answer(i18n.get("premium_stars_text", premium_stars=premium_stars, nl=nl))

is_get_id = True	
is_get_score = True

@router_score.message(Command("get_score"))
async def get_score_admin(message: Message, i18n: I18nContext):
	if message.from_user.id == 1240754158:
		global is_get_id
		is_get_id = True
		await message.answer("Введи id кому ти хочеш надіслати зірочки!")
		@router_score.message(lambda message: is_get_id)
		async def is_get_id_func(message: Message):
			global is_get_id, is_get_score
			id = int(message.text)
			is_get_id = False
			is_get_score = True
			await message.answer("Напиши кількість зірочок!")
			@router_score.message(lambda message: is_get_score)
			async def is_get_score_func(message: Message, i18n: I18nContext):
				global is_get_score
				numbers_of_stars = int(message.text)
				cursor.execute("SELECT score FROM game WHERE id = ?", (id,))
				score = cursor.fetchone()[0]
				cursor.execute("UPDATE game SET score = ? WHERE id = ?", (score + numbers_of_stars, id,))
				conn.commit()
				await message.answer("Зірочки надіслані! Команда тільки для адмінів!")
				is_get_score = False
				await bot.send_message(id, i18n.get("sented_scores"))


@router_score.message(Command("id"))
async def get_id(message: Message):
	await message.answer(f"{message.from_user.id}")
	