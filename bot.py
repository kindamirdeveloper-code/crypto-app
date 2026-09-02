import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils import executor

API_TOKEN = '8664121709:AAGZLrm7vwV2uY8n6HKrPOtqsP6olCPJeEc'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

MINI_APP_URL = "https://kindamirdeveloper-code.github.io/crypto-app/"

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    web_app_btn = InlineKeyboardButton(
        text="🚀 ورود به بازار زنده (مینی‌اپ)", 
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    refresh_info_btn = InlineKeyboardButton(
        text="🔄 راهنمای به‌روزرسانی", 
        callback_data="refresh_help"
    )
    keyboard.add(web_app_btn, refresh_info_btn)

    await message.answer(
        "سلام! به ربات تحلیل و قیمت لحظه‌ای کریپتو خوش آمدید.\n\n"
        "برای مشاهده قیمت‌های زنده و پویای بازار (با آپدیت ۲ ثانیه‌ای)، روی دکمه زیر کلیک کنید:",
        reply_markup=keyboard
    )

@dp.callback_query_handler(text="refresh_help")
async def process_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        "💡 قیمت‌ها داخل مینی‌اپ به‌صورت خودکار هر ۲ ثانیه یک‌بار آپدیت می‌شوند. همچنین می‌توانید از دکمه‌ی رفرش بالای صفحه مینی‌اپ استفاده کنید."
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
