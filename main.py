from fastapi import FastAPI
import sqlite3
from database import init_db, save_or_update_user

# فرض بر این است که از FastAPI برای مینی‌اپ استفاده می‌کنی
app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

# مسیر API برای تحویل لیست کاربران به مینی‌اپ
@app.get("/api/get_users")
def get_users():
    conn = sqlite3.connect('bot_database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, first_name, last_seen, session_count FROM users ORDER BY last_seen DESC")
    rows = cursor.fetchall()
    conn.close()
    
    users_list = [dict(row) for row in rows]
    return {"status": "success", "users": users_list}

# مثال نحوه استفاده هنگام استارت خوردن ربات توسط کاربر (در هندلر استارت ربات تلگرام):
def handle_user_start(message):
    user = message.from_user
    save_or_update_user(user.id, user.username, user.first_name)
