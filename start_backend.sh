#!/bin/bash
echo "Iniciando entorno..."

# Activar entorno virtual
source back-model/venv/bin/activate

# Abrir Redis en nueva ventana desde la ruta especificada
gnome-terminal -- bash -c "cd '/home/bryam/Imágenes/Septimo_ciclo/Aprendisage Automatico/hola/STOCKY-IA/Redis-x64-3.0.504/' && redis-server; exec bash"

# Espera para que Redis arranque
sleep 5

# Iniciar FastAPI en nueva ventana
gnome-terminal -- bash -c "cd back-model && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000; exec bash"

# Iniciar Celery en nueva ventana
gnome-terminal -- bash -c "cd back-model && source venv/bin/activate && celery -A core.celery_config.celery_app worker --loglevel=info --pool=solo -Q training-queue; exec bash"

echo "Todo levantado. Puedes cerrar esta ventana si deseas."
pause

