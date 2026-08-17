from typing import Optional

from pydantic import BaseModel, Field


class Restaurant(BaseModel):
    
    name: str
    location: str
    type: str
    food_style: str
    rating: Optional[float] = None
    price_range: Optional[float] = None
    signatures: list[str] = Field(default_factory=list)
    vibe: Optional[str] = None
    environment: str
    shortcomings: list[str] = Field(default_factory=list)