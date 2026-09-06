import sqlite3

def init_db():
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_seen DATETIME,
            session_count INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

def save_or_update_user(user_id, username, first_name):
    conn = sqlite3.connect('bot_database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_id, username, first_name, last_seen, session_count)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP, 1)
        ON CONFLICT(user_id) DO UPDATE SET 
            last_seen = CURRENT_TIMESTAMP,
            session_count = session_count + 1
    ''', (user_id, username, first_name))
    conn.commit()
    conn.close()
