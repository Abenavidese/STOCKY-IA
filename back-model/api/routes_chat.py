# back-model/api/routes_chat.py
from fastapi import APIRouter
from models.chat_message import ChatMessage
import json

router = APIRouter()

# Ruta para recibir los mensajes del chat y guardarlos en un archivo JSON
@router.post("/")
async def save_message(chat_message: ChatMessage):
    try:
        with open('messages.json', 'r') as file:
            messages = json.load(file)
    except FileNotFoundError:
        messages = []

    messages.append(chat_message.dict())

    # Guardar los mensajes actualizados en el archivo JSON
    with open('messages.json', 'w') as file:
        json.dump(messages, file, indent=4)

    return {"status": "success", "message": "Mensaje guardado"}
