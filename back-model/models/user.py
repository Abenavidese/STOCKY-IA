from pydantic import BaseModel, EmailStr

# Modelo que recibe frontend
class UserLogin(BaseModel):
    email: EmailStr

# Modelo que devuelve el backend con ID generado
class UserResponse(BaseModel):
    user_id: str
    email: EmailStr
    username: str