import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "general.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_db_and_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabla usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        username TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Tabla productos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()
