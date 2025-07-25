from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import json
import pandas as pd  # NECESARIO PARA pd.to_datetime

Base = declarative_base()

class Prediccion(Base):
    __tablename__ = "predicciones"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    fecha = Column(String, index=True)
    product_id = Column(Integer, index=True)
    product_name = Column(String)
    category_id = Column(Integer)
    category_name = Column(String)
    prediccion = Column(Float)
    venta_anterior = Column(Float)
    price_usd = Column(Float)  # NUEVO CAMPO
    historico = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db_session(user_id: str):
    """
    Devuelve una sesión de DB específica para el usuario.
    """
    user_id = user_id.strip()  
    user_dir = os.path.join("models", user_id)
    os.makedirs(user_dir, exist_ok=True)
    db_path = os.path.join(user_dir, "predicciones.db")

    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Crear tabla si no existe
    Base.metadata.create_all(bind=engine)
    return SessionLocal()



def guardar_predicciones_en_db(df_pred, df_hist, user_id):
    db = get_db_session(user_id)
    try:
        for _, row in df_pred.iterrows():
            hist_data = df_hist[
                (df_hist['product_id'] == row['product_id']) &
                (pd.to_datetime(df_hist['dt_target']).dt.date == pd.to_datetime(row['fecha']).date())
            ]

            hist_row = hist_data.iloc[0].to_dict() if not hist_data.empty else {}

            for key, value in hist_row.items():
                if isinstance(value, pd.Timestamp):
                    hist_row[key] = value.strftime("%Y-%m-%d")

            hist_json = json.dumps(hist_row) if hist_row else None

            # Verificar si ya existe predicción para este producto y fecha
            existing_pred = db.query(Prediccion).filter_by(
                user_id=user_id,
                product_id=row['product_id'],
                fecha=row['fecha']
            ).first()

            if existing_pred:
                # Actualizamos en vez de duplicar
                existing_pred.prediccion = row['prediccion']
                existing_pred.venta_anterior = row.get('venta_anterior', None)
                existing_pred.price_usd = row.get('price_usd', None)
                existing_pred.historico = hist_json
            else:
                # Creamos nuevo registro
                pred = Prediccion(
                    user_id=user_id,
                    fecha=row['fecha'],
                    product_id=row['product_id'],
                    product_name=row.get('product_name', 'N/A'),
                    category_id=row.get('category_id', None),
                    category_name=row.get('category_name', 'N/A'),
                    prediccion=row['prediccion'],
                    venta_anterior=row.get('venta_anterior', None),
                    price_usd=row.get('price_usd', None),
                    historico=hist_json
                )
                db.add(pred)

        db.commit()
    finally:
        db.close()

