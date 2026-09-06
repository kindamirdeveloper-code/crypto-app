import sqlite3

def save_or_update_user(user_id, username, first_name):
    conn = sqlite3.connect('bot_database.db')
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
