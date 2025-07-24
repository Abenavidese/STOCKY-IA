from fastapi import APIRouter, HTTPException
from models.schemas import ChatMessage
from database.crud import get_or_create_thread, save_message, get_conversation_history, get_db_connection
from services.openai_service import get_openai_response
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/message")
async def chat(msg: ChatMessage):
    logger.info(f"Mensaje recibido de user {msg.userId} ({msg.username}) sobre producto {msg.productId}")

    if not msg.message.strip():
        raise HTTPException(status_code=400, detail="Mensaje vacío")

    # 1. Obtener o crear hilo de conversación
    thread_id = get_or_create_thread(msg.userId)

    # 2. Guardar mensaje del usuario
    save_message(thread_id, "user", msg.message)

    # 3. Preparar prompt con contexto enriquecido
    contexto = msg.contexto
    historico = contexto.historico.dict()  # si es modelo Pydantic

    # Construir texto con datos del contexto para el prompt
    historico_texto = "\n".join(
        f"- {key}: {value}" for key, value in historico.items()
    )

    prompt = f"""
Eres un asistente experto en predicción de demanda y gestión de inventarios para retail.  
Recibes datos de ventas ya ajustados para representar unidades reales (valores ya están desnormalizados).  
Redondea estos valores al número entero más cercano antes de analizarlos.

Variables disponibles:
- rolling_mean_sale_7: Promedio de ventas de los últimos 7 días.
- rolling_mean_sale_3: Promedio de ventas de los últimos 3 días.
- max_last_5: Máximo de ventas en los últimos 5 días.
- day_of_week: Día de la semana (0=Lunes, 6=Domingo).
- weekly_day_avg: Promedio de ventas de ese día en las últimas 4 semanas.
- prev_day_sale: Ventas del día anterior.
- sale_amount: Ventas reales del día actual (objetivo).

ten en cuenta también estos datos

Producto: {contexto.productName}
Categoría: {contexto.categoryName}
Fecha: {msg.fecha}
Predicción: {contexto.prediccion}
Venta anterior: {contexto.ventaAnterior}
Precio USD: {contexto.priceUsd}
Fecha creación predicción: {contexto.createdAt}

Datos históricos relevantes:
{historico_texto}

Pregunta del usuario: {msg.message}

*Tu tarea:*
1. Interpreta la situación actual (por ejemplo, ¿las ventas están subiendo o bajando?).
2. Da recomendaciones prácticas sobre el stock (ejemplo: “considera aumentar stock el fin de semana”).
3. Sé claro, preciso y habla en términos de negocio (sin jerga técnica).
4. Resalta solo los valores más relevantes (predicción y ventas pasadas ya desnormalizadas).
5. No describas el modelo ni la IA, enfócate en la información útil para el negocio.
6. No nombres que estás multiplicando por 7 las variables que te pido, solo centrate en aconsejar al negocio de forma útil sobre su predicción.
"""

    # 4. Construir el historial para OpenAI con prompt inicial y mensajes previos
    conversation_history = get_conversation_history(thread_id)

    messages = [
        {"role": "system", "content": "Eres un asistente experto en ventas y predicción de stock."},
        {"role": "user", "content": prompt}
    ]

    # Opcionalmente agregar conversación previa (si quieres usar contexto más extenso)
    messages.extend(conversation_history)

    # 5. Consultar OpenAI
    answer = get_openai_response(messages)

    # 6. Guardar respuesta del asistente
    save_message(thread_id, "assistant", answer)

    return {
        "status": "success",
        "thread_id": thread_id,
        "response": answer,
        "conversation_history": get_conversation_history(thread_id)
    }

@router.get("/conversation/{thread_id}")
async def get_conversation(thread_id: str):
    # Verificar si el hilo existe en la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT thread_id FROM threads WHERE thread_id = ?", (thread_id,))
    thread_exists = cursor.fetchone()
    conn.close()

    if not thread_exists:
        raise HTTPException(status_code=404, detail="Hilo no encontrado")

    # Obtener el historial de conversación
    conversation_history = get_conversation_history(thread_id)

    return {
        "thread_id": thread_id,
        "conversation_history": conversation_history
    }