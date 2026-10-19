from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, ARRAY, text

class ItemBase(SQLModel):
    name: str = Field(index=True)
    brand: str = Field(sa_column=Column(String, nullable=False, server_default=text("'Unknown'")))
    quantity: int = Field(default=0, ge=0)
    price: float = Field(gt=0)
    category: str
    img_url: str
    tags: list[str] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String), nullable=False, server_default=text("'{}'"))        
    )      
class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")


class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int  
    owner_id: int