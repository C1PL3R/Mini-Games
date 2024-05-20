from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram_i18n import I18nContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType
from database import *
from config import PROVIDER_TOKEN

router_pay = Router()

nl="\n"

@router_pay.message(Command("buy"))
async def order_cmd(message: Message, bot: Bot, i18n: I18nContext):
    prices=[]
    cursor.execute("SELECT premium FROM game WHERE id = ?", (message.from_user.id,))
    premium = cursor.fetchone()[0]
    if premium == 0:
        nl="\n"
        description = i18n.get("buy_text_descrption_not_premium", nl=nl)
        prices=[
            LabeledPrice(
                label=i18n.get("buy_text_label2"),
                amount=550
            )
        ]
    else:
        nl="\n"
        description=i18n.get("buy_text_descrption", nl=nl)
        prices=[
            LabeledPrice(
                label=i18n.get("buy_text_label1"),
                amount=500
            )
        ]
    await message.answer_invoice(
        title=i18n.get("buy_text_title"),
        description=description,
        payload="buy_premium",
        provider_token=PROVIDER_TOKEN,
        currency="UAH",
        prices=[LabeledPrice(
                label=i18n.get("buy_text_label1"),
                amount=500
            )],
        start_parameter="buy",
        provider_data=None,
        need_name=True,
        need_email=True,
        need_phone_number=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=True,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=15,
    )

@router_pay.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@router_pay.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message, i18n: I18nContext):
    cursor.execute("SELECT premium_stars FROM game WHERE id = ?", (message.from_user.id,))
    premium_stars = cursor.fetchone()[0]
    cursor.execute("SELECT premium FROM game WHERE id = ?", (message.from_user.id,))
    premium = cursor.fetchone()[0]

    if premium == 1:
        text = "buy_successful"
        cursor.execute("UPDATE game SET premium_stars = ? WHERE id = ?", (premium_stars + 10, message.from_user.id,))
        conn.commit()
    else:
        text= "buy_successful_not_premium"
        cursor.execute("UPDATE game SET premium = ? WHERE id = ?", (1, message.from_user.id,))
        conn.commit()
    cursor.execute("SELECT premium_stars FROM game WHERE id = ?", (message.from_user.id,))
    premium_stars = cursor.fetchone()[0]

    await message.answer(i18n.get(text, name=message.from_user.mention_html(), 
                                  total_amount=message.successful_payment.total_amount * 0.01, 
                                  currency=message.successful_payment.currency, 
                                  premium_stars=premium_stars,
                                  nl=nl), parse_mode="html")


is_get_premium = True
@router_pay.message(Command("get_premium"))
async def order(message: Message):
    if message.from_user.id == 1240754158:
        global is_get_premium
        is_get_premium = True
        mess = await message.answer("Введи id кому ти хочеш активувати Premium!")
        @router_pay.message(lambda message: is_get_premium)
        async def is_get_id_func(message: Message):
            global is_get_premium
            id = int(message.text)
            cursor.execute("UPDATE game SET premium = ? WHERE id = ?", (1, id,))
            conn.commit()
            cursor.execute("SELECT link FROM game WHERE id = ?", (id,))
            link = cursor.fetchone()[0]
            await message.answer(f"Преміум активовано коритувачеві @{link}")
            is_get_premium = False

