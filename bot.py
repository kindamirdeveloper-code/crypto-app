import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession

API_TOKEN = '8664121709:AAGZLrm7vwV2uY8n6HKrPOtqsP6olCPJeEc'

logging.basicConfig(level=logging.INFO)

# تنظیم پروکسی مخصوص اکانت‌های رایگان PythonAnywhere
session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot(token=API_TOKEN, session=session)
dp = Dispatcher()

MINI_APP_URL = "https://kindamirdeveloper-code.github.io/crypto-app/"

WELCOME_TEXT = (
    "👋 Welcome to **Crypto-View** Live Market & Analytics Bot!\n\n"
    "🚀 Your ultimate companion for real-time crypto tracking:\n\n"
    "📈 **Key Features:**\n"
    "• Live pricing for 100+ top coins (2-second updates)\n"
    "• Advanced TradingView charts\n"
    "• Personalized Watchlist for your favorite assets\n"
    "• Smart Price Alert system with instant notifications\n\n"
    "Click the button below to launch the live market 👇"
)
BTN_TEXT = "🚀 Open Live Market (Mini App)"

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=BTN_TEXT, web_app=types.WebAppInfo(url=MINI_APP_URL))]
    ])
    await message.answer(WELCOME_TEXT, reply_markup=keyboard, parse_mode='Markdown')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
