import pandas as pd
import numpy as np
import os
import joblib
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, InputLayer
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

# --- Parámetros del modelo ---
SEQ_LENGTH = 5
BATCH_SIZE = 128
EPOCHS = 5

def create_sequences(X, y, product_ids, dts, seq_length):
    """
    Genera secuencias de longitud seq_length para cada producto,
    incluyendo la fecha (dt) asociada al target.
    """
    X_seq, y_seq, prod_seq, dt_seq = [], [], [], []
    for i in range(len(X) - seq_length):
        if product_ids[i:i+seq_length].nunique() == 1:
            X_seq.append(X[i:i+seq_length])
            y_seq.append(y[i + seq_length])
            prod_seq.append(product_ids.iloc[i + seq_length])
            dt_seq.append(dts.iloc[i + seq_length])  # Guardar la fecha objetivo
    return np.array(X_seq), np.array(y_seq), np.array(prod_seq), np.array(dt_seq)

def train_lstm_model(user_id: str, csv_path: str):
    print(f"[TRAINING] Iniciando con archivo: {csv_path}")

    try:
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"El archivo CSV no existe: {csv_path}")

        df = pd.read_csv(csv_path, parse_dates=["dt"])
        if df.empty:
            raise ValueError("El archivo CSV está vacío.")

        # --- Preprocesamiento ---
        df['dt'] = pd.to_datetime(df['dt'])
        df = df.sort_values(['product_id', 'dt'])

        df['rolling_mean_sale_7'] = df.groupby('product_id')['sale_amount'].transform(lambda x: x.shift(1).rolling(7).mean())
        df['rolling_mean_sale_3'] = df.groupby('product_id')['sale_amount'].transform(lambda x: x.shift(1).rolling(3).mean())
        df['max_last_5'] = df.groupby('product_id')['sale_amount'].transform(lambda x: x.shift(1).rolling(5).max())
        df['day_of_week'] = df['dt'].dt.dayofweek
        df['weekly_day_avg'] = df.groupby(['product_id', 'day_of_week'])['sale_amount'].transform(lambda x: x.shift(1).rolling(4).mean())
        df['prev_day_sale'] = df.groupby('product_id')['sale_amount'].shift(1)

        df = df.dropna().reset_index(drop=True)

        # --- Directorio de modelos ---
        model_dir = f"models/{user_id}"
        os.makedirs(model_dir, exist_ok=True)

        # --- Guardar df procesado ---
        df_processed_path = f"{model_dir}/df_processed.csv"
        df.to_csv(df_processed_path, index=False)
        print(f"[INFO] DataFrame procesado guardado en: {df_processed_path}")

        # --- Features ---
        features = [
            'rolling_mean_sale_7',
            'weekly_day_avg',
            'rolling_mean_sale_3',
            'max_last_5',
            'prev_day_sale'
        ]
        target = 'sale_amount'

        df_selected = df[features + [target, 'product_id', 'dt']]

        X = df_selected[features]
        y = df_selected[target]

        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)

        # --- Crear secuencias con fechas ---
        X_seq, y_seq, prod_seq, dt_seq = create_sequences(
            X_scaled, y.values, df_selected['product_id'], df_selected['dt'], SEQ_LENGTH
        )

        if len(X_seq) == 0:
            raise ValueError("No se pudieron crear secuencias válidas para entrenamiento.")

        # --- Guardar histórico de secuencias ---
        seq_feature_names = [f"{feat}_t{i}" for i in range(SEQ_LENGTH) for feat in features]
        X_seq_flat = X_seq.reshape(X_seq.shape[0], -1)
        df_hist_seq = pd.DataFrame(X_seq_flat, columns=seq_feature_names)
        df_hist_seq['target_y'] = y_seq
        df_hist_seq['product_id'] = prod_seq
        df_hist_seq['dt_target'] = dt_seq  # NUEVA COLUMNA

        hist_seq_path = f"{model_dir}/historical_sequences.csv"
        df_hist_seq.to_csv(hist_seq_path, index=False)
        print(f"[INFO] Histórico de secuencias guardado en: {hist_seq_path}")

        # --- Dividir train/val ---
        split_index = int(len(X_seq) * 0.85)
        X_train, X_val = X_seq[:split_index], X_seq[split_index:]
        y_train, y_val = y_seq[:split_index], y_seq[split_index:]

        # --- Modelo LSTM ---
        model = Sequential([
            InputLayer(input_shape=(SEQ_LENGTH, len(features))),
            LSTM(64, return_sequences=False),
            Dropout(0.1),
            Dense(20, activation='relu', kernel_initializer='he_normal'),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])

        # --- Callbacks ---
        model_path = f"{model_dir}/model.keras"
        scaler_path = f"{model_dir}/scaler.save"

        early_stop = EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6, verbose=1)
        checkpoint = ModelCheckpoint(model_path, monitor='val_loss', save_best_only=True, verbose=1)

        # --- Entrenamiento ---
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            callbacks=[early_stop, reduce_lr, checkpoint],
            verbose=1
        )

        # --- Guardar scaler ---
        joblib.dump(scaler, scaler_path)

        print(f"[SUCCESS] Modelo guardado en: {model_path}")
        return model_path, scaler_path, hist_seq_path

    except Exception as e:
        print(f"[ERROR ENTRENAMIENTO]: {e}")
        return None, None, None
