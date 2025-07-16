from fastapi import APIRouter, HTTPException
from models.user import UserLogin, UserResponse
from database.crud import get_user_by_email, create_user
import uuid

router = APIRouter()

def extract_username(email: str) -> str:
    return email.split('@')[0]

@router.post("/login", response_model=UserResponse)
def login(user: UserLogin):
    # Buscar usuario en BD
    existing_user = get_user_by_email(user.email)
    if existing_user:
        return UserResponse(
            user_id=existing_user['user_id'],
            email=existing_user['email'],
            username=existing_user['username']
        )
    
    # Si no existe, crear nuevo usuario con un nuevo ID
    new_id = str(uuid.uuid4())
    username = extract_username(user.email)
    # Supongamos que password viene en UserLogin, o lo manejas aparte
    # Aquí debes definir un password dummy o requerirlo
    dummy_password = "changeme123"  # Mejor pedir contraseña real y hacer hash
    create_user(new_id, user.email, username, dummy_password)
    
    return UserResponse(user_id=new_id, email=user.email, username=username)

@router.get("/login")
def get_users():
    return [
        {"user_id": uid, "email": udata["email"], "username": udata["username"]}
        for uid, udata in users_db.items()
    ]