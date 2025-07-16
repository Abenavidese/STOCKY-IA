from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import pandas as pd
from services.prediction import predecir_para_fecha
from tensorflow.keras.models import load_model
import joblib
from fastapi.responses import FileResponse
from fpdf import FPDF
from datetime import datetime

router = APIRouter()

class PredictionRequest(BaseModel):
    fecha: str
    user_id: str

# --- Función para generar el PDF (sin cambios) ---
def generar_pdf_predicciones(df_predicciones: pd.DataFrame, fecha_objetivo: str, output_path: str):
    """
    Genera un PDF con las predicciones para todos los productos en la fecha indicada.
    """
    try:
        fecha = pd.to_datetime(fecha_objetivo).date()
    except ValueError:
        raise ValueError("Formato de fecha inválido. Use AAAA-MM-DD.")

    df_fecha = df_predicciones[pd.to_datetime(df_predicciones['fecha']).dt.date == fecha]

    if df_fecha.empty:
        raise ValueError(f"No hay predicciones para la fecha {fecha_objetivo}")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Reporte de Predicciones - {fecha.strftime('%d/%m/%Y')}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 10, "Producto ID", border=1, align="C")
    pdf.cell(40, 10, "Predicción", border=1, align="C")
    pdf.cell(45, 10, "Venta Mes Anterior", border=1, align="C")
    pdf.ln()

    pdf.set_font("Arial", '', 10)
    for _, row in df_fecha.iterrows():
        prediccion_redondeada = round(row['prediccion'])
        pdf.cell(40, 10, str(row['product_id']), border=1)
        pdf.cell(40, 10, str(prediccion_redondeada), border=1, align="C")
        pdf.cell(45, 10, f"{row.get('venta_anterior', 'N/A'):.2f}", border=1, align="R")
        pdf.ln()

    pdf.output(output_path)
    return output_path

@router.post("/predict/pdf")
def predict_and_save_pdf(request: PredictionRequest): # Cambié el nombre para mayor claridad
    try:
        # --- Lógica de predicción (sin cambios) ---
        model_dir = f"models/{request.user_id}"
        model_path = f"{model_dir}/model.keras"
        scaler_path = f"{model_dir}/scaler.save"
        df_path = f"{model_dir}/df_processed.csv"

        if not os.path.exists(model_path) or not os.path.exists(scaler_path) or not os.path.exists(df_path):
            raise HTTPException(status_code=404, detail="Modelo, scaler o DataFrame no encontrados.")

        model = load_model(model_path)
        scaler = joblib.load(scaler_path)
        df = pd.read_csv(df_path, parse_dates=['dt'])

        df_pred = predecir_para_fecha(df, request.fecha, model, scaler)

        if df_pred.empty:
            raise HTTPException(status_code=404, detail=f"No se pudieron generar predicciones para la fecha {request.fecha}.")

        # --- CAMBIO 1: Definir la ruta de guardado ---
        # El PDF se guardará dentro de la carpeta del modelo del usuario.
        # Esto sobrescribirá el archivo 'informe.pdf' en cada llamada.
        pdf_output_path = f"{model_dir}/informe.pdf"
        
        # Llama a tu función para crear el archivo PDF en esa ruta
        generar_pdf_predicciones(df_pred, request.fecha, pdf_output_path)

        # --- CAMBIO 2: Devolver una respuesta JSON de éxito ---
        return {
            "status": "ok",
            "message": f"Informe de predicciones guardado en: {pdf_output_path}"
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {str(e)}")
    
# --- Endpoint que DEBES AÑADIR ---
# Endpoint 2: Sirve el PDF ya guardado
@router.get("/download/report/{user_id}")
def download_report(user_id: str):
    pdf_path = f"models/{user_id}/informe.pdf"
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Informe PDF no encontrado. Genérelo primero.")
    
    return FileResponse(
        path=pdf_path,
        media_type='application/pdf',
        filename=f"informe_predicciones_{user_id}.pdf"
    )