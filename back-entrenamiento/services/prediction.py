import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from datetime import datetime
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
    df['dt'] = pd.to_datetime(df['dt'], errors='coerce')
    df = df.dropna(subset=['dt'])

    if df['dt'].isna().sum() > 0:
        raise ValueError("Hay valores de fecha no válidos en el DataFrame.")

    # Ordenar por producto y fecha
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

        # Crear entrada para el modelo
        X_input = scaler.transform(df_seq[FEATURES])
        X_input = X_input.reshape((1, seq_length, len(FEATURES)))
        y_pred = model.predict(X_input, verbose=0)[0][0]

        # Datos del producto
        product_name = df_prod['product_name'].iloc[0] if 'product_name' in df_prod.columns else f"Producto {prod_id}"
        category_id = df_prod['category_id'].iloc[0] if 'category_id' in df_prod.columns else "N/A"
        category_name = df_prod['category_name'].iloc[0] if 'category_name' in df_prod.columns else "N/A"

        # Obtener el último precio disponible
        price_usd = df_hist['price_usd'].iloc[-1] if 'price_usd' in df_hist.columns else None

        predicciones.append({
            'product_id': prod_id,
            'product_name': product_name,
            'category_id': category_id,
            'category_name': category_name,
            'fecha': fecha_str,
            'venta_anterior': round(df_hist.iloc[-2]['sale_amount'], 2) if len(df_hist) > 1 else 'N/A',
            'prediccion': round(y_pred, 2),
            'price_usd': float(price_usd) if price_usd is not None else None
        })

    return pd.DataFrame(predicciones)
