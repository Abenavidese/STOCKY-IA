from .connection import get_db_connection
import hashlib

# ------------------ Usuarios ------------------

def hash_password(password: str) -> str:
    # Para simplificar, hash sha256; en producción usa bcrypt o similar
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_user(user_id: str, email: str, username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = hash_password(password)
    cursor.execute(
        'INSERT INTO users (user_id, email, username, password_hash) VALUES (?, ?, ?, ?)',
        (user_id, email, username, password_hash)
    )
    conn.commit()
    conn.close()

def get_user_by_email(email: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, email, username FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, email, username FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_user_password(email: str, password: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return False
    return hash_password(password) == row['password_hash']

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, email, username FROM users')
    rows = cursor.fetchall()
    conn.close()
    return rows

# ------------------ Productos ------------------

def create_product(product_id: str, product_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO products (product_id, product_name) VALUES (?, ?)',
        (product_id, product_name)
    )
    conn.commit()
    conn.close()

def get_product_by_id(product_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT product_id, product_name FROM products WHERE product_id = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT product_id, product_name FROM products')
    rows = cursor.fetchall()
    conn.close()
    return rows
