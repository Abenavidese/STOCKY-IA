# backend-modelo/services/training.py

import pandas as pd
from darts import TimeSeries
from darts.models import Prophet
from datetime import datetime
import joblib
import os

def train_with_darts(user_id: str, csv_path: str):
    print(f"[TRAINING] Iniciando con archivo: {csv_path}")

    try:
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"El archivo CSV no existe: {csv_path}")

        df = pd.read_csv(csv_path, parse_dates=["dt"])

        if "dt" not in df.columns or "sale_amount" not in df.columns:
            raise ValueError("El CSV debe contener las columnas 'dt' y 'sale_amount'.")

        if df.empty:
            raise ValueError("El archivo CSV está vacío.")
        

        df_agg = df.groupby("dt")["sale_amount"].sum().reset_index()

        ts = TimeSeries.from_dataframe(df_agg, "dt", "sale_amount")

        model = Prophet()
        model.fit(ts)

        model_id = datetime.now().strftime("%Y%m%d%H%M%S")
        model_dir = f"models/{user_id}"
        os.makedirs(model_dir, exist_ok=True)
        model_path = f"{model_dir}/{model_id}.pkl"

        joblib.dump(model, model_path)
        print(f"[SUCCESS] Modelo guardado en: {model_path}")

        return model_path, model_id

    except Exception as e:
        print(f"[ERROR ENTRENAMIENTO]: {e}")
        return None, None
