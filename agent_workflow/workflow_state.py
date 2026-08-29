
from typing import TypedDict
from langchain_core.documents import Document


class WorkflowState(TypedDict):
    
    user_id: str
    query: str
    user_reviews: list[dict]
    user_profile: dict
    
    retrieved_restaurants: list[dict]
    retrieved_recipes: list[Document]
    retrieved_reviews: list[Document]
    
    food_analyst: str
    
    final_recommendationL: list[dict]
    