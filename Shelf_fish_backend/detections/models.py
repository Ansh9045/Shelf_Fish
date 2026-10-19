from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, ARRAY, text

class LLMOutput(SQLModel):
    name: str
    brand: str
    category: str
    tags: list[str] = Field(
        description="At least 3-5 lowercase keywords a shopper might search to find this exact product. Never return an empty list."
    )

class DetectionBase(SQLModel):
    name: Optional[str]
    brand: Optional[str]
    category: Optional[str]
    img_url: Optional[str]
    tags: list[str] = Field(
                default_factory=list,
                sa_column=Column(ARRAY(String), nullable=False, server_default=text("'{}'"))        
            ) 

class Detection(DetectionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    user_id: Optional[int] = Field(foreign_key="user.id")

class DetectionRead(DetectionBase):
    id: int
    created_at: datetime
    user_id: int