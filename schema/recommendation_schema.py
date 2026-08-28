

from pydantic import BaseModel

class RestaurantRecommendation(BaseModel):
    
    restaurant: str
    cuisine: str
    dish: str
    location: str
    
    
class RecommendationResponse(BaseModel):
    
    response: list[RestaurantRecommendation]