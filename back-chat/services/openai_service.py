from openai import OpenAI
import os
import logging
from dotenv import load_dotenv
from httpx import HTTPStatusError

load_dotenv()

logger = logging.getLogger(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY no está configurada")
    raise RuntimeError("OPENAI_API_KEY no está configurada en las variables de entorno")

client = OpenAI(api_key=api_key)

def get_openai_response(messages: list, model="gpt-4o-mini", max_tokens=600, temperature=0.7):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except HTTPStatusError as e:
        if e.response.status_code == 429:
            logger.error(f"Límite de cuota alcanzado: {e.response.text}")
            return "Error: Se ha alcanzado el límite de cuota de OpenAI. Por favor, inténtalo más tarde."
        else:
            raise
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        raise
