from fastapi import APIRouter, HTTPException
from services.database import get_db_session, Prediccion
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/int_predictions/{user_id}")
def get_predicciones(user_id: str):
    """
    Devuelve todas las predicciones guardadas en la base de datos
    para un usuario, incluyendo el campo 'fecha' para cada predicción.
    """
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
                "created_at": r.created_at
            }
            data.append(record)
        return data
    finally:
        session.close()
