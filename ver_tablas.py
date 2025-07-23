import os
import pandas as pd
from sqlalchemy import create_engine

# Ruta de la DB
db_path = r"C:\Users\EleXc\Videos\STOCKY-IA\STOCKY-DEV\back-entrenamiento\models\123\predicciones.db"

if not os.path.exists(db_path):
    raise FileNotFoundError(f"No se encontró la base de datos en: {db_path}")

# Conexión a SQLite
engine = create_engine(f"sqlite:///{db_path}")

# Leer la tabla 'predicciones'
df = pd.read_sql_table("predicciones", con=engine)

print("\n--- Registros en la DB ---\n")
print(df.head(20))  # Muestra los primeros 20 registros
print("\nTotal de registros:", len(df))
