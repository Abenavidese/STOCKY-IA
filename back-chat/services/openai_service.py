from openai import OpenAI
import os
import logging
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

logger = logging.getLogger(__name__)

# Obtener la clave de API desde las variables de entorno
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY no está configurada")
    raise RuntimeError("OPENAI_API_KEY no está configurada en las variables de entorno")

client = OpenAI(api_key=api_key)

def get_openai_response(messages: list, model="gpt-3.5-turbo", max_tokens=300, temperature=0.7):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error en OpenAI: {e}")
        raise
