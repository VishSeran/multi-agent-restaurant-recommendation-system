
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    
    user_id: str 
    
    prefered_cuisines: list[str] = Field(default_factory=list)
    
    preferred_foods: list[str] = Field(default_factory=list)
    
    preferred_food_traite: list[str] = Field(default_factory=list)
    
    atmosphere_preferences: list[str] = Field(default_factory=list)
    
    disliked_atmosphere: list[str] = Field(default_factory=list)
    
    dietary_preferences: list[str] = Field(default_factory=list)
    
    price_perference: str|None = None
    
    additional_preferences: list[str] = Field(default_factory=list) 