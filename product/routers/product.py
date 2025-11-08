from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas
from ..database import get_db
from ..routers.login import get_current_user

router = APIRouter(
    prefix="/product",
    tags=["Product"]
)

# ---------------- CREATE PRODUCT ----------------
@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
def create_product(request: schemas.Product, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    new_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price,
    )
    db.add(new_product)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create product")
    db.refresh(new_product)
    return new_product

@router.options("/create")
def create_product_options():
    return Response()

# ---------------- GET ALL PRODUCTS ----------------
@router.get("/all", response_model=List[schemas.Product])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

# ---------------- GET PRODUCT BY ID ----------------
@router.get("/{id}", response_model=schemas.Product)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.get(models.Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# ---------------- UPDATE PRODUCT ----------------
@router.put("/update/{id}")
def update_product(id: int, updated_data: schemas.Product, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    product = db.get(models.Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in updated_data.model_dump().items():
        setattr(product, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to update product")
    db.refresh(product)
    return {"message": "Product updated successfully", "data": product}

@router.options("/update/{id}")
def update_product_options():
    return Response()

# ---------------- DELETE PRODUCT ----------------
@router.delete("/delete/{id}")
def delete_product(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    product = db.get(models.Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.options("/delete/{id}")
def delete_product_options():
    return Response()
