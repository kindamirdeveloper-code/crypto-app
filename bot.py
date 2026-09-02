import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession

API_TOKEN = '8664121709:AAGZLrm7vwV2uY8n6HKrPOtqsP6olCPJeEc'

logging.basicConfig(level=logging.INFO)

# تنظیم پروکسی مخصوص اکانت‌های رایگان PythonAnywhere
session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot(token=API_TOKEN, session=session)
dp = Dispatcher()

MINI_APP_URL = "https://kindamirdeveloper-code.github.io/crypto-app/"

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🚀 ورود به بازار زنده (مینی‌اپ)", web_app=types.WebAppInfo(url=MINI_APP_URL))],
        [types.InlineKeyboardButton(text="🔄 راهنمای به‌روزرسانی", callback_data="refresh_help")]
    ])
    
    await message.answer(
        "سلام! به ربات تحلیل و قیمت لحظه‌ای کریپتو خوش آمدید.\n\n"
        "برای مشاهده قیمت‌های زنده و پویای بازار (با آپدیت ۲ ثانیه‌ای)، روی دکمه زیر کلیک کنید:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "refresh_help")
async def process_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(
        "💡 قیمت‌ها داخل مینی‌اپ به‌صورت خودکار هر ۲ ثانیه یک‌بار آپدیت می‌شوند. همچنین می‌توانید از دکمه‌ی رفرش بالای صفحه مینی‌اپ استفاده کنید."
    )

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
