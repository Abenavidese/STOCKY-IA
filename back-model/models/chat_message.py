from pydantic import BaseModel

class ChatMessage(BaseModel):
    productId: str
    productName: str  
    message: str
