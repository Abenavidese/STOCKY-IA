from fastapi import APIRouter, HTTPException
from models.chat_message import ChatMessage
import httpx

router = APIRouter()

messages_storage = []

@router.post("/")
async def receive_chat_message(msg: ChatMessage):
    messages_storage.append(msg)
    print(f"Mensaje recibido: {msg}")

    url_chat_backend = "http://localhost:8001/api/message"  # Cambia puerto y URL si es necesario

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url_chat_backend, json=msg.dict())
            response.raise_for_status()
            backend_response = response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error al conectar con backend chat: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=response.status_code, detail=f"Error del backend chat: {e}")

    return {
        "status": "ok",
        "received_message": msg.dict(),
        "chat_backend_response": backend_response
    }

@router.get("/")
async def get_all_messages():
    return {"messages": [m.dict() for m in messages_storage]}
