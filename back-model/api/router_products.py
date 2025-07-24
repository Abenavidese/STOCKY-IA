from fastapi import APIRouter, HTTPException
from models.product import ProductCreate, ProductResponse
from database.crud import get_product_by_id, create_product

router = APIRouter()

@router.post("/products", response_model=ProductResponse)
def add_product(product: ProductCreate):
    existing = get_product_by_id(product.product_id)
    if existing:
        if existing['product_name'] != product.product_name:
            raise HTTPException(
                status_code=400,
                detail=f"Conflicto: el producto ID '{product.product_id}' ya existe con nombre '{existing['product_name']}'"
            )
        # Producto ya existe con mismo nombre, retornamos sin error
        return ProductResponse(product_id=product.product_id, product_name=product.product_name)
    create_product(product.product_id, product.product_name)
    return ProductResponse(product_id=product.product_id, product_name=product.product_name)

