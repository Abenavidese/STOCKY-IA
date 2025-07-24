from fastapi import FastAPI
from routers import chat
from fastapi.middleware.cors import CORSMiddleware
from database.connection import create_db_and_tables
from routers.chat import router as chat_router

app = FastAPI()

origins = [
    "http://localhost:4200",  # URL del frontend Angular
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],      # Permitir todos los métodos (GET, POST, OPTIONS...)
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_db_and_tables()

app.include_router(chat_router, prefix="/api/chat")

