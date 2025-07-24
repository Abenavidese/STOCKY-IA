from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from services.database import get_db_session, Prediccion
import pandas as pd

analytics_router = APIRouter()

@analytics_router.get("/analytics/{user_id}")
def get_analytics(user_id: str):
    session: Session = get_db_session(user_id)
    try:
        results = session.query(Prediccion).all()
        if not results:
            raise HTTPException(status_code=404, detail="No se encontraron predicciones")

        # --- Convertir los registros a DataFrame ---
        data = [
            {
                "fecha": r.fecha,
                "product_id": r.product_id,
                "product_name": r.product_name,
                "category_id": r.category_id,
                "category_name": r.category_name,
                "prediccion": r.prediccion,
                "price_usd": getattr(r, "price_usd", 1.0)
            }
            for r in results
        ]
        df = pd.DataFrame(data)

        # --- Ajustar predicciones ---
        df["prediccion"] = (df["prediccion"] * 7)
        df["ventas_usd"] = (df["prediccion"] * df["price_usd"])

        # --- 1. Ventas totales por categoría ---
        ventas_por_categoria = df.groupby("category_name")["ventas_usd"].sum().sort_values(ascending=False).to_dict()

        # --- 2. Top 5 productos ---
        productos_ordenados = df.groupby("product_name")["ventas_usd"].sum().sort_values(ascending=False).round(2)
        top_productos = productos_ordenados.head(5).to_dict()

        # --- 2b. Productos menos consumidos ---
        productos_menos_consumidos = productos_ordenados.tail(5).to_dict()

        # --- 3. Serie de tiempo de ventas (por fecha) ---
        ventas_tiempo = (
            df.groupby("fecha")["ventas_usd"].sum()
            .reset_index()
            .to_dict(orient="records")
        )

        # --- 4. Estadísticas adicionales ---
        ventas_totales = df["ventas_usd"].sum().round(2)
        ventas_promedio_dia = df.groupby("fecha")["ventas_usd"].sum().mean().round(2)
        producto_top = productos_ordenados.idxmax()
        distribucion_precios = df["price_usd"].describe().round(2).to_dict()

        return {
            "ventas_por_categoria": ventas_por_categoria,
            "top_productos": top_productos,
            "productos_menos_consumidos": productos_menos_consumidos,
            "ventas_tiempo": ventas_tiempo,
            "ventas_totales_usd": ventas_totales,
            "ventas_promedio_dia": ventas_promedio_dia,
            "producto_top": producto_top,
            "distribucion_precios": distribucion_precios
        }

    finally:
        session.close()
