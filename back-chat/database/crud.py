from .connection import get_db_connection
import time

# Hilos
def get_or_create_thread(user_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT thread_id FROM threads WHERE user_id = ? ORDER BY created_at DESC LIMIT 1', (user_id,))
    thread = cursor.fetchone()
    if thread:
        thread_id = thread[0]
    else:
        thread_id = f"thread_{user_id}_{int(time.time())}"
        cursor.execute('INSERT INTO threads (thread_id, user_id) VALUES (?, ?)', (thread_id, user_id))
        conn.commit()
    conn.close()
    return thread_id

# Mensajes
def save_message(thread_id: str, role: str, content: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (thread_id, role, content) VALUES (?, ?, ?)', (thread_id, role, content))
    conn.commit()   
    conn.close()

def get_conversation_history(thread_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT role, content FROM messages WHERE thread_id = ? ORDER BY timestamp ASC', (thread_id,))
    messages = cursor.fetchall()
    conn.close()
    return [{"role": m[0], "content": m[1]} for m in messages]

def get_all_threads():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM threads")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY timestamp ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows
