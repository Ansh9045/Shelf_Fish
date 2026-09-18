from typing import Optional
from sqlmodel import SQLModel, Field

class ItemBase(SQLModel):
    name: str = Field(index=True)
    quantity: int = Field(default=0, ge=0)
    price: float = Field(gt=0)
    category: str
      
class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")


class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int  
    owner_id: int