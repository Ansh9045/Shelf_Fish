from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class LLMOutput(SQLModel):
    name: str
    brand: str
    category: str

class DetectionBase(SQLModel):
    name: Optional[str]
    brand: Optional[str]
    category: Optional[str]

class Detection(DetectionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    user_id: Optional[int] = Field(foreign_key="user.id")

class DetectionRead(DetectionBase):
    id: int
    created_at: datetime
    user_id: int