from fastapi import FastAPI
from routers import chat
from database.connection import create_db_and_tables
from routers.chat import router as chat_router

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

app.include_router(chat_router, prefix="/api")

