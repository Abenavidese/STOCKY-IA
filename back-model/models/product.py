from pydantic import BaseModel

class ProductCreate(BaseModel):
    product_id: str
    product_name: str

class ProductResponse(BaseModel):
    product_id: str
    product_name: str