from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, ARRAY, text
from enum import Enum
from pydantic import field_validator

class Tier(str, Enum):
    essential = "essential"
    useful = "useful"
    want = "want"

MAX_NORM = 30



class LLMOutput(SQLModel):
    name: str
    brand: str
    category: str
    tags: list[str] = Field(
        description="At least 3-5 lowercase keywords a shopper might search to find this exact product. Never return an empty list."
    )
    tier: Tier = Field(
        description= "Rationing tier for product, essential: basic necessities, useful: items that improve quality of life, want: luxury items. Use 'want' if unsure or unknown."
    )
    ration_norm: int = Field(
        description= "Units a person would reasonably need in a week. Integer, at least 1"
    )
    @field_validator("tier", mode="before")
    @classmethod
    def validate_tier(cls, v):
        if isinstance(v, Tier):
            return v
        try:
            return Tier(str(v).strip().lower())
        except ValueError:
            return Tier.want

    @field_validator("ration_norm", mode="before")
    @classmethod
    def validate_norm(cls, v):
        try:
            n = int(v)
        except (TypeError, ValueError):
            n= 1

        return max(1, min(n, MAX_NORM))

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, v):
        out = []
        for t in v:
            t = t.strip().lower()
            if t and t not in out:
                out.append(t)

        return out



class DetectionBase(SQLModel):
    name: Optional[str]
    brand: Optional[str]
    category: Optional[str]
    img_url: Optional[str]
    tags: list[str] = Field(
                default_factory=list,
                sa_column=Column(ARRAY(String), nullable=False, server_default=text("'{}'"))        
            )
    tier: str = Field(
        default= "want",
        sa_column_kwargs={"server_default" : "want"}
    )
    ration_norm: int = Field(
        default = 1,
        sa_column_kwargs={"server_default" : "1"}
    )

class Detection(DetectionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    user_id: Optional[int] = Field(foreign_key="user.id")

class DetectionRead(DetectionBase):
    id: int
    created_at: datetime
    user_id: int