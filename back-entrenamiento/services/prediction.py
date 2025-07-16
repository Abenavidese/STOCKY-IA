import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from datetime import datetime
from fpdf import FPDF
import os

SEQ_LENGTH = 5
FEATURES = [
    'rolling_mean_sale_7',
    'weekly_day_avg',
    'rolling_mean_sale_3',
    'max_last_5',
    'prev_day_sale'
]
def predecir_para_fecha(df, fecha_str, model, scaler, seq_length=SEQ_LENGTH):
    # Aseguramos que la columna 'dt' sea tipo datetime
    df['dt'] = pd.to_datetime(df['dt'], errors='coerce')  # Coerce para manejar errores de conversión
    df = df.dropna(subset=['dt'])  # Eliminar filas donde la fecha no pudo ser convertida

    # Verificar si la conversión fue exitosa
    if df['dt'].isna().sum() > 0:
        raise ValueError("Hay valores de fecha no válidos en el DataFrame.")

    # Ordenar los datos por 'product_id' y 'dt'
    df = df.sort_values(['product_id', 'dt'])

    fecha_obj = pd.to_datetime(fecha_str).date()
    predicciones = []

    for prod_id in df['product_id'].unique():
        df_prod = df[df['product_id'] == prod_id].sort_values('dt')
        df_hist = df_prod[df_prod['dt'].dt.date <= fecha_obj]

        if len(df_hist) < seq_length:
            continue

        df_seq = df_hist.iloc[-seq_length:]
        if df_seq['dt'].max().date() != fecha_obj:
            continue

        X_input = scaler.transform(df_seq[FEATURES])
        X_input = X_input.reshape((1, seq_length, len(FEATURES)))
        y_pred = model.predict(X_input, verbose=0)[0][0]

        predicciones.append({
            'product_id': prod_id,
            'fecha': fecha_str,
            'prediccion': round(y_pred, 2),
            'venta_anterior': df_hist.iloc[-2]['sale_amount'] if len(df_hist) > 1 else 'N/A'
        })

    return pd.DataFrame(predicciones)  # Devuelve solo las predicciones
