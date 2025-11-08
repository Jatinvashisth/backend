from pydantic import BaseModel, EmailStr
from typing import Optional

class UserDataSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str

    class Config:
        from_attributes = True  # Pydantic v2

class DisplayUser(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
