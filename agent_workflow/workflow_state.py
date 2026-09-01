
from typing import TypedDict
from langchain_core.documents import Document

from retriever.restaurant_retriever import RestaurantRetriever
from schema.relevance_schema import RelevanceSchema
from vectore_store.images_db import ImageVectorDB
from vectore_store.restaurants_db import RestaurantVectorDB


class WorkflowState(TypedDict):
    
    user_id: str
    query: str
    image_query: str | None
    user_reviews: list[dict]
    user_profile: dict
    
    retrieved_restaurants: list[dict]
    retrieved_content: str
    retrieved_recipes: list[Document]
    retrieved_reviews: list[Document]
    
    relevancy_response : RelevanceSchema
    relevance_result: str
    
    food_analyst: str
    
    final_recommendation: list[dict]
    