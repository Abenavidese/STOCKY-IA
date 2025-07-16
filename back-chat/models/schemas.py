from pydantic import BaseModel

class ChatMessage(BaseModel):
    userId: str
    username: str
    productId: str
    productName: str  
    message: str