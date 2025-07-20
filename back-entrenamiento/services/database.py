from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

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
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db_session(user_id: str):
    """
    Devuelve una sesión de DB específica para el usuario.
    """
    # Eliminar espacios y saltos de línea
    user_id = user_id.strip()  

    user_dir = os.path.join("models", user_id)
    os.makedirs(user_dir, exist_ok=True)
    db_path = os.path.join(user_dir, "predicciones.db")

    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Crear tabla si no existe
    Base.metadata.create_all(bind=engine)
    return SessionLocal()

def guardar_predicciones_en_db(df_pred, user_id):
    db = get_db_session(user_id)
    try:
        for _, row in df_pred.iterrows():
            pred = Prediccion(
                user_id=user_id,
                fecha=row['fecha'],
                product_id=row['product_id'],
                product_name=row.get('product_name', 'N/A'),
                category_id=row.get('category_id', None),
                category_name=row.get('category_name', 'N/A'),
                prediccion=row['prediccion'],
                venta_anterior=row.get('venta_anterior', None)
            )
            db.add(pred)
        db.commit()
    finally:
        db.close()
