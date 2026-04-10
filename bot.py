import asyncio
import logging
import os

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
CallbackQuery,
InlineKeyboardButton,
InlineKeyboardMarkup,
LabeledPrice,
Message,
PreCheckoutQuery,
)
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(**name**)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
WEBHOOK_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
PORT = int(os.environ.get("PORT", 10000))

WEBHOOK_PATH = “/webhook”
WEBHOOK_URL = f”https://{WEBHOOK_HOST}{WEBHOOK_PATH}”

WELCOME_TEXT = (
“🎁✨ Приветствуем тебя! ✨🎁\n\n”
“Хочешь радовать себя и других крутыми подарками, но не переплачивать? “
“Тогда ты точно по адресу! 😎\n\n”
“🔥 В нашем боте ты можешь купить подарки дешевле, чем где-либо\n”
“⚡ Моментальная отправка — без ожидания и лишних действий\n”
“💫 Подарки можно:\n”
“— обменять на ⭐ звезды\n”
“— сохранить в профиле как коллекцию\n”
“— или сразу отправить близким\n\n”
“🎉 Это не просто покупки — это эмоции, внимание и удовольствие в пару кликов!\n\n”
“🚀 Присоединяйся прямо сейчас и начни дарить радость выгодно!”
)

AFTER_PAYMENT_TEXT = (
“🎁✨ Хочешь получить свой подарок? Всё максимально просто! ✨🎁\n\n”
“💬 Напиши прямо сюда — и мы быстро оформим для тебя подарок без лишних ожиданий!\n\n”
“⚡ Мгновенная выдача\n”
“🎉 Приятные бонусы и эмоции\n”
“⭐ Возможность обменять или сохранить\n\n”
“Не откладывай — забери свой подарок уже сейчас и порадуй себя или близких 💫\n”
“@wopst”
)

GIFTS = [
{“label”: “🧸/💝 10 ⭐️”, “stars”: 10, “callback”: “buy_10”},
{“label”: “🌹/🎁 20 ⭐️”, “stars”: 20, “callback”: “buy_20”},
{“label”: “💐/🍾/🎂/🚀 35 ⭐️”, “stars”: 35, “callback”: “buy_35”},
{“label”: “💍/💎/🏆 60 ⭐️”, “stars”: 60, “callback”: “buy_60”},
]

def get_main_keyboard() -> InlineKeyboardMarkup:
buttons = [
[InlineKeyboardButton(text=gift[“label”], callback_data=gift[“callback”])]
for gift in GIFTS
]
buttons.append(
[InlineKeyboardButton(text=“🆘 Поддержка”, url=“https://t.me/wopst”)]
)
return InlineKeyboardMarkup(inline_keyboard=buttons)

dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
await message.answer(text=WELCOME_TEXT, reply_markup=get_main_keyboard())

@dp.callback_query(F.data.in_({“buy_10”, “buy_20”, “buy_35”, “buy_60”}))
async def handle_buy(callback: CallbackQuery, bot: Bot) -> None:
stars_map = {“buy_10”: 10, “buy_20”: 20, “buy_35”: 35, “buy_60”: 60}
stars = stars_map[callback.data]

```
title_map = {
    10: "🧸/💝 Подарок — 10 звёзд",
    20: "🌹/🎁 Подарок — 20 звёзд",
    35: "💐/🍾/🎂/🚀 Подарок — 35 звёзд",
    60: "💍/💎/🏆 Подарок — 60 звёзд",
}

await bot.send_invoice(
    chat_id=callback.from_user.id,
    title=title_map[stars],
    description="Покупка подарка в Telegram Stars",
    payload=f"gift_{stars}",
    currency="XTR",
    prices=[LabeledPrice(label="Оплата", amount=stars)],
)
await callback.answer()
```

@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery, bot: Bot) -> None:
await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message) -> None:
await message.answer(text=AFTER_PAYMENT_TEXT)

async def on_startup(bot: Bot) -> None:
await bot.set_webhook(WEBHOOK_URL)
logger.info(f”Webhook set: {WEBHOOK_URL}”)

async def on_shutdown(bot: Bot) -> None:
await bot.delete_webhook()
logger.info(“Webhook deleted”)

async def main() -> None:
if not BOT_TOKEN:
raise ValueError(“BOT_TOKEN is not set”)

```
bot = Bot(token=BOT_TOKEN)

dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)

app = web.Application()
handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
handler.register(app, path=WEBHOOK_PATH)
setup_application(app, dp, bot=bot)

runner = web.AppRunner(app)
await runner.setup()
site = web.TCPSite(runner, host="0.0.0.0", port=PORT)
await site.start()
logger.info(f"Server started on port {PORT}")

await asyncio.Event().wait()
```

if **name** == “**main**”:
asyncio.run(main())
