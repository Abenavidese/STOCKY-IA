from fastapi import APIRouter, HTTPException
from services.database import get_db_session, Prediccion
from sqlalchemy.orm import Session
import json

router = APIRouter()

@router.get("/int_predictions/{user_id}")
def get_predicciones(user_id: str):
    session: Session = get_db_session(user_id)
    try:
        results = session.query(Prediccion).order_by(Prediccion.fecha.desc()).all()

        if not results:
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontraron predicciones para el usuario {user_id}"
            )

        data = []
        for r in results:
            record = {
                "id": r.id,
                "user_id": r.user_id,
                "fecha": r.fecha,
                "product_id": r.product_id,
                "product_name": r.product_name,
                "category_id": r.category_id,
                "category_name": r.category_name,
                "prediccion": r.prediccion,
                "venta_anterior": r.venta_anterior,
                "price_usd": r.price_usd,  # NUEVO
                "created_at": r.created_at,
                "historico": json.loads(r.historico) if r.historico else {}
            }
            data.append(record)
        return data
    finally:
        session.close()
