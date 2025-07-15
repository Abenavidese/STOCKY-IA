from fastapi import FastAPI, HTTPException, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
import logging
import sqlite3
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY no está configurada")
    raise RuntimeError("OPENAI_API_KEY no está configurada en las variables de entorno")

client = OpenAI(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_db():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS threads (
        thread_id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        thread_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (thread_id) REFERENCES threads (thread_id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT NOT NULL,
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()

def insert_sample_products():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    sample_products = [
        ("prod_001", "Manzana Roja", "Manzanas frescas y jugosas."),
        ("prod_002", "Banana", "Bananas maduras para consumo inmediato."),
        ("prod_003", "Leche Entera", "Leche fresca entera, 1 litro."),
    ]
    cursor.executemany("INSERT OR IGNORE INTO products (product_id, product_name, description) VALUES (?, ?, ?)", sample_products)
    conn.commit()
    conn.close()

create_db()
insert_sample_products()

class LoginRequest(BaseModel):
    user_id: str

class MessageRequest(BaseModel):
    user_id: str
    message: str
    product_id: str = "No especificado"

def get_or_create_user(user_id: str, username: str):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.execute('INSERT INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
        conn.commit()
        print(f"[DB] Nuevo usuario creado: user_id={user_id}, username={username}")
    else:
        print(f"[DB] Usuario existente encontrado: user_id={user_id}")
    
    conn.close()

def get_or_create_thread(user_id: str):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    
    cursor.execute('''SELECT thread_id FROM threads WHERE user_id = ? ORDER BY created_at DESC LIMIT 1''', (user_id,))
    thread = cursor.fetchone()
    
    if thread:
        thread_id = thread[0]
        print(f"[DB] Hilo existente recuperado: thread_id={thread_id} para user_id={user_id}")
    else:
        thread_id = f"thread_{user_id}_{int(time.time())}"
        cursor.execute('INSERT INTO threads (thread_id, user_id) VALUES (?, ?)', (thread_id, user_id))
        conn.commit()
        print(f"[DB] Nuevo hilo creado: thread_id={thread_id} para user_id={user_id}")
    
    conn.close()
    return thread_id

def save_message(thread_id: str, role: str, content: str):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (thread_id, role, content) VALUES (?, ?, ?)', (thread_id, role, content))
    conn.commit()
    print(f"[DB] Mensaje guardado: thread_id={thread_id}, role={role}, content={content[:50]}{'...' if len(content)>50 else ''}")
    conn.close()

def get_conversation_history(thread_id: str):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT role, content FROM messages WHERE thread_id = ? ORDER BY timestamp ASC', (thread_id,))
    messages = cursor.fetchall()
    print(f"[DB] Historial recuperado para thread_id={thread_id}, total mensajes={len(messages)}")
    conn.close()
    return messages

def get_product_info(product_id: str):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, description FROM products WHERE product_id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    if product:
        return f"Producto: {product[0]}. Descripción: {product[1]}"
    return "Producto desconocido."

class UserLoginRequest(BaseModel):
    user_id: str
    username: str

@app.post("/login")
async def login(request: dict = Body(...)):
    username = request.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="Username es requerido")
    
    # Buscar usuario por username
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    
    if row:
        user_id = row[0]
        print(f"[DB] Usuario existente encontrado: username={username}, user_id={user_id}")
    else:
        # Crear nuevo user_id
        user_id = f"user_{int(time.time())}"
        cursor.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()
        print(f"[DB] Nuevo usuario creado: username={username}, user_id={user_id}")
    conn.close()
    
    thread_id = get_or_create_thread(user_id)
    conversation_history = get_conversation_history(thread_id)
    
    return {
        "user_id": user_id,
        "thread_id": thread_id,
        "conversation_history": [{"role": role, "content": content} for role, content in conversation_history]
    }

@app.get("/api/products")
async def list_products():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, product_name, description FROM products")
    products = cursor.fetchall()
    conn.close()
    
    return [
        {"product_id": p[0], "product_name": p[1], "description": p[2]}
        for p in products
    ]


@app.post("/api/message")
async def chat(req: MessageRequest):
    logger.info(f"Message received - User: {req.user_id}, Product: {req.product_id}")
    
    if not req.message.strip():
        logger.warning("Mensaje vacío recibido")
        raise HTTPException(status_code=400, detail="Mensaje vacío")
    
    thread_id = get_or_create_thread(req.user_id)
    save_message(thread_id, "user", req.message)
    conversation_history = get_conversation_history(thread_id)
    product_context = get_product_info(req.product_id)
    
    try:
        messages = [{"role": "system", "content": "Eres un asistente experto en ventas y predicción de stock."},
                    {"role": "system", "content": f"Información del producto: {product_context}"}]
        
        for role, content in conversation_history:
            messages.append({"role": role, "content": content})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        
        answer = response.choices[0].message.content
        logger.info("Respuesta de OpenAI recibida exitosamente")
        
        save_message(thread_id, "assistant", answer)
        
        return {
            "status": "success",
            "user_id": req.user_id,
            "thread_id": thread_id,
            "response": answer,
            "product_id": req.product_id
        }
    except Exception as e:
        logger.error(f"Error de OpenAI: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al comunicarse con OpenAI: {str(e)}")

@app.get("/api/conversation/{thread_id}")
async def get_conversation(thread_id: str = Path(...)):
    conversation_history = get_conversation_history(thread_id)
    # No retornes 404 si está vacío, solo si el hilo no existe realmente.
    # Para eso puedes verificar si el hilo existe en la tabla threads.
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT thread_id FROM threads WHERE thread_id = ?", (thread_id,))
    thread_exists = cursor.fetchone()
    conn.close()

    if not thread_exists:
        raise HTTPException(status_code=404, detail="Hilo no encontrado")

    return {
        "thread_id": thread_id,
        "conversation_history": [{"role": role, "content": content} for role, content in conversation_history]
    }
