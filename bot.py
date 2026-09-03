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

# ذخیره زبان انتخابی کاربران
user_languages = {}

TEXTS = {
    'fa': {
        'welcome': (
            "👋 به ربات تحلیل و قیمت لحظه‌ای **Crypto-View** خوش آمدید!\n\n"
            "🚀 همراه مطمئن شما برای رصد زنده و پویا بازار ارزهای دیجیتال:\n\n"
            "📈 **امکانات اصلی ربات:**\n"
            "• مشاهده قیمت‌های لحظه‌ای بیش از ۱۰۰ ارز دیجیتال برتر (آپدیت ۲ ثانیه‌ای)\n"
            "• دسترسی به نمودارهای پیشرفته TradingView\n"
            "• ساخت واچ‌لیست شخصی‌سازی‌شده از ارزهای مورد علاقه\n"
            "• سیستم هوشمند هشدار قیمت (Price Alert) با ارسال نوتیفیکیشن مستقیم\n\n"
            "جهت ورود به بازار زنده، روی دکمه زیر کلیک کنید 👇"
        ),
        'btn_text': "🚀 ورود به بازار زنده (مینی‌اپ)"
    },
    'en': {
        'welcome': (
            "👋 Welcome to **Crypto-View** Live Market & Analytics Bot!\n\n"
            "🚀 Your ultimate companion for real-time crypto tracking:\n\n"
            "📈 **Key Features:**\n"
            "• Live pricing for 100+ top coins (2-second updates)\n"
            "• Advanced TradingView charts\n"
            "• Personalized Watchlist for your favorite assets\n"
            "• Smart Price Alert system with instant notifications\n\n"
            "Click the button below to launch the live market 👇"
        ),
        'btn_text': "🚀 Open Live Market (Mini App)"
    }
}

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    lang = user_languages.get(user_id, 'fa')
    
    text = TEXTS[lang]['welcome']
    btn_text = TEXTS[lang]['btn_text']

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=btn_text, web_app=types.WebAppInfo(url=MINI_APP_URL))]
    ])

    await message.answer(text, reply_markup=keyboard, parse_mode='Markdown')

# دریافت اطلاعات ارسالی از مینی‌اپ (تغییر زبان و هشدارهای قیمت)
@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        user_id = message.from_user.id
        action = data.get('action')
        
        if action == 'set_lang':
            selected_lang = data.get('lang', 'fa')
            user_languages[user_id] = selected_lang
        elif action == 'alert_triggered':
            alert_msg = data.get('message')
            if alert_msg:
                await message.answer(alert_msg)
    except Exception as e:
        logging.error(f"Error handling web_app_data: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
