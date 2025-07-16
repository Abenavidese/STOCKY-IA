import requests
import os
from uuid import uuid4

def obtener_csvs_disponibles():
    response = requests.get("http://localhost:8000/api/datasets/files")
    if response.status_code != 200:
        raise Exception("No se pudo obtener la lista de CSVs")

    archivos_remotos = response.json()
    temp_dir = "temp_downloads"
    os.makedirs(temp_dir, exist_ok=True)

    archivos_locales = []

    for ruta_remota in archivos_remotos:
        ruta_normalizada = ruta_remota.replace("\\", "/")  # ← esta línea es clave
        nombre_local = f"{uuid4()}.csv"
        local_path = os.path.join(temp_dir, nombre_local)

        url = f"http://localhost:8000/api/datasets/files/download?path={ruta_normalizada}"
        r = requests.get(url)

        if r.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(r.content)
            archivos_locales.append(local_path)
        else:
            print(f"[ERROR] No se pudo descargar: {ruta_remota}")

    return archivos_locales
