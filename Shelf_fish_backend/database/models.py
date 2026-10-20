from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, ARRAY, text, CheckConstraint, UniqueConstraint
from detections.models import Tier, MAX_NORM
from pydantic import field_validator


class ItemBase(SQLModel):
    name: str = Field(index=True)
    brand: str = Field(sa_column=Column(String, nullable=False, server_default=text("'Unknown'")))
    quantity: int = Field(default=0, ge=0)
    category: str
    img_url: str
    tags: list[str] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String), nullable=False, server_default=text("'{}'"))        
    )      
    tier: str = Field(default="want", sa_column_kwargs={"server_default": "want"})
    ration_norm: int = Field(default=1, ge=1, le=MAX_NORM, sa_column_kwargs={"server_default": "1"})

class Item(ItemBase, table=True):
    __table_args__ = (CheckConstraint("quantity >=0", name="check_quantity_non_neg"),
                      CheckConstraint("ration_norm >=1", name="check_ration_norm_non_neg"),
                      UniqueConstraint("name", "brand", name="uq_item")
                      )
    id: Optional[int] = Field(default=None, primary_key=True)
    contributed_by : Optional[int] = Field(foreign_key="user.id")


class ItemCreate(ItemBase):
    quantity: int = Field(default=1, ge=1)
    detection_id: Optional[int] = None

    @field_validator("tier")
    @classmethod
    def real_name(cls, v):
        v= " ".join(v.split())
        if not v or v.lower() == "unknown":
            raise ValueError("Please enter a valid name for this item.")
        return v

    @field_validator("brand")
    @classmethod
    def clean_brand(cls, v):
        v = " ".join(v.split())
        return "Unknown" if not v or v.lower() =="unknown" else v
    

class ItemRead(ItemBase):
    id: int  
    owner_id: int