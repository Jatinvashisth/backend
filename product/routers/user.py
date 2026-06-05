from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from .login import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user_details(
    request: schemas.UserCreateDetails,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
    current_user.username = request.name
    current_user.email = request.email
    current_user.phone = request.phone
    current_user.address = request.address

    db.commit()
    db.refresh(current_user)

    return {"message": "User details saved successfully"}



@router.get("/details")
def get_user_details(
    current_user: models.User = Depends(get_current_user)
):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "phone": current_user.phone,
        "address": current_user.address
    }


