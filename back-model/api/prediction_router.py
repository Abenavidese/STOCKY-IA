from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import httpx

router = APIRouter()

# URL de tu OTRO backend (el del modelo). Ajusta el puerto si es necesario.
MODEL_BACKEND_URL = "http://127.0.0.1:8002 " # Asumiendo que corre en el puerto 8001

@router.get("/report/download/{user_id}/{fecha}")
async def get_and_download_report(user_id: str, fecha: str):
    """
    Este endpoint orquesta la generación y descarga del reporte:
    1. Llama al backend del modelo para generar el PDF.
    2. Llama de nuevo para descargar ese PDF.
    3. Lo retransmite (stream) al frontend.
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Paso A: Pedir la generación del PDF
            print(f"Pidiendo al modelo que genere el reporte para user: {user_id}")
            gen_response = await client.post(
                f"{MODEL_BACKEND_URL}/api/prediction/predict/pdf",
                json={"user_id": user_id, "fecha": fecha}
            )
            gen_response.raise_for_status() # Lanza error si la generación falla

            # Paso B: Descargar el PDF ya generado
            print(f"Descargando el reporte desde el modelo...")
            dl_response = await client.get(
                f"{MODEL_BACKEND_URL}/api/prediction/download/report/{user_id}"
            )
            dl_response.raise_for_status() # Lanza error si la descarga falla

            # Paso C: Retransmitir el archivo al frontend
            return StreamingResponse(
                dl_response.aiter_bytes(),
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename=reporte_{user_id}_{fecha}.pdf"}
            )

        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="No se pudo comunicar con el servicio de modelos.")
        except httpx.HTTPStatusError as e:
            # Propagar el error del microservicio al frontend
            raise HTTPException(status_code=e.response.status_code, detail=e.response.json().get("detail"))