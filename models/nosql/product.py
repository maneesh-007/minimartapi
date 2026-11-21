from datetime import datetime, timezone
from typing import Optional
from beanie import Document
from pydantic import Field


class Product(Document):
    name: str
    price:float
    status:bool
    description:str 
    originalPrice: float
    category: str
    rating: float
    reviews: int
    badge: str
    image:str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "product"        # collection name