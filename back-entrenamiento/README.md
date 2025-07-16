puerto backend del modelo 

uvicorn main:app --reload --port 8002

iniciar angular

ng serve

puerto del backend general 

uvicorn main:app --reload

inicio del celery en redis

python -m celery -A worker.celery_app worker --loglevel=info -Q training-queue --pool=solo