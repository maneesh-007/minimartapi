from datetime import datetime, timezone
from typing import Optional
from beanie import Document
from pydantic import Field


class Category(Document):

    name:str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "category"
