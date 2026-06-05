from pydantic import BaseModel, EmailStr
from typing import Optional


class UserDataCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserDataSchema(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str



class UserCreateDetails(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True
