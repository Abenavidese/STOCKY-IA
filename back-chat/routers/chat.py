from fastapi import APIRouter, HTTPException
from models.schemas import ChatMessage
from database.crud import get_or_create_thread, save_message, get_conversation_history
from services.openai_service import get_openai_response
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/message")
async def chat(msg: ChatMessage):    
    logger.info(f"Mensaje recibido de user {msg.userId} ({msg.username}) sobre producto {msg.productId}")

    if not msg.message.strip():
        raise HTTPException(status_code=400, detail="Mensaje vacío")

    # 3. Obtener o crear hilo
    thread_id = get_or_create_thread(msg.userId)

    # 4. Guardar mensaje del usuario
    save_message(thread_id, "user", msg.message)

    # 5. Preparar historial para enviar a OpenAI
    conversation_history = get_conversation_history(thread_id)
    messages = [
        {"role": "system", "content": "Eres un asistente experto en ventas y predicción de stock."}
    ]
    messages.extend(conversation_history)

    # 6. Obtener respuesta de OpenAI
    answer = get_openai_response(messages)

    # 7. Guardar respuesta del asistente
    save_message(thread_id, "assistant", answer)

    return {
        "status": "success",
        "thread_id": thread_id,
        "response": answer,
        "conversation_history": get_conversation_history(thread_id)
    }


@router.get("/api/conversation/{thread_id}")
async def get_conversation(thread_id: str):
    conversation_history = get_conversation_history(thread_id)
    # Verificar si hilo existe
    from database.connection import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT thread_id FROM threads WHERE thread_id = ?", (thread_id,))
    thread_exists = cursor.fetchone()
    conn.close()

    if not thread_exists:
        raise HTTPException(status_code=404, detail="Hilo no encontrado")

    return {
        "thread_id": thread_id,
        "conversation_history": conversation_history
    }
