import json
import os
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

TOKEN = "8664121709:AAGZLrm7vwV2uY8n6HKrPOtqsP6olCPJeEc"
ADMIN_ID = (
    8443620164
)
WEBAPP_URL ="https://kindamirdeveloper-code.github.io/crypto-app/"

bot = telebot.TeleBot(TOKEN)
CHANNELS_FILE = "channels.json"


def load_channels():
  if not os.path.exists(CHANNELS_FILE):
    return []
  with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
    return json.load(f)


def save_channels(channels):
  with open(CHANNELS_FILE, "w", encoding="utf-8") as f:
    json.dump(channels, f, ensure_ascii=False)


def check_membership(user_id):
  channels = load_channels()
  for ch in channels:
    try:
      member = bot.get_chat_member(ch, user_id)
      if member.status not in ["member", "administrator", "creator"]:
        return False
    except:
      return False
  return True


@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_id = message.from_user.id
  if not check_membership(user_id):
    channels = load_channels()
    markup = InlineKeyboardMarkup()
    for ch in channels:
      markup.add(
          InlineKeyboardButton(f"📢 عضویت در {ch}", url=f"https://t.me/{ch[1:]}")
      )
    markup.add(
        InlineKeyboardButton(
            "✅ عضو شدم، بررسی مجدد", callback_data="check_join"
        )
    )
    bot.send_message(
        message.chat.id,
        "❌ برای استفاده از مینی‌اپ، ابتدا باید در کانال‌های زیر عضو شوید:",
        reply_markup=markup,
    )
    return

  markup = InlineKeyboardMarkup()
  markup.add(
      InlineKeyboardButton(
          "🚀 باز کردن مینی‌اپ قیمت‌ها", web_app=WebAppInfo(url=WEBAPP_URL)
      )
  )
  bot.send_message(
      message.chat.id,
      "سلام! برای مشاهده قیمت لحظه‌ای ارزها و طلا روی دکمه زیر کلیک کنید:",
      reply_markup=markup,
  )


@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def callback_check(call):
  if check_membership(call.from_user.id):
    bot.answer_callback_query(call.id, "عضویت شما تایید شد! ✅")
    try:
      bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
      pass
    send_welcome(call.message)
  else:
    bot.answer_callback_query(
        call.id, "هنوز در همه کانال‌ها عضو نشده‌اید!", show_alert=True
    )


# دستورات ادمین برای مدیریت کانال‌ها
@bot.message_handler(commands=["add"])
def add_channel(message):
  if message.from_user.id != ADMIN_ID:
    return
  args = message.text.split()
  if len(args) < 2:
    bot.reply_to(message, "فرمت صحیح: /add @channelusername")
    return
  ch = args[1]
  channels = load_channels()
  if ch not in channels:
    channels.append(ch)
    save_channels(channels)
    bot.reply_to(message, f"کانال {ch} به لیست عضویت اجباری اضافه شد.")
  else:
    bot.reply_to(message, "این کانال از قبل در لیست وجود دارد.")


@bot.message_handler(commands=["del"])
def del_channel(message):
  if message.from_user.id != ADMIN_ID:
    return
  args = message.text.split()
  if len(args) < 2:
    bot.reply_to(message, "فرمت صحیح: /del @channelusername")
    return
  ch = args[1]
  channels = load_channels()
  if ch in channels:
    channels.remove(ch)
    save_channels(channels)
    bot.reply_to(message, f"کانال {ch} از لیست حذف شد.")
  else:
    bot.reply_to(message, "کانال مورد نظر پیدا نشد.")


print("Bot is running...")
bot.infinity_polling()