from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    full_name: str

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed: str

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserRead(UserBase):
    id: int

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"