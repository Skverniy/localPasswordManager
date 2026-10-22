from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class VaultItemCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    username: str = Field(default="", max_length=200)
    url: str = Field(default="", max_length=500)
    password: str = Field(..., min_length=1, max_length=500)
    notes: str = Field(default="", max_length=10000)


class VaultItemUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    username: Optional[str] = Field(default=None, max_length=200)
    url: Optional[str] = Field(default=None, max_length=500)
    password: Optional[str] = Field(default=None, min_length=1, max_length=500)
    notes: Optional[str] = Field(default=None, max_length=10000)


class VaultItemResponse(BaseModel):
    id: int
    title: str
    username: str
    url: str
    notes: str
    created_at: datetime
    updated_at: datetime


class RevealResponse(BaseModel):
    password: str