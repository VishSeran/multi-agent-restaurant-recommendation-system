
from langchain_core.prompts import ChatPromptTemplate

from configurations.logger import get_logger
from llms.llm_handler import LLMHandler
from schema.recommendation_schema import RecommendationResponse


logger = get_logger("recommendation-agent")

class RecommendationAgent:
    
    def __init__(self):
        
        try:
            
            self.llm_handler = LLMHandler(temperature=0.3)
            self.llm = self.llm_handler.get_llm().with_structured_output(RecommendationResponse)
            
            self.prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                     """
                    You are an expert restaurant recommendation agent.

                    Your task is to recommend the most suitable restaurants based on:
                    - The user's query and preferences
                    - Retrieved restaurant information
                    - Restaurant rankings and relevance scores
                    - Food context provided by the food agent
                    - Cuisine, location, rating, price range, and other available information

                    Use the restaurant context to determine which restaurants can be recommended.
                    Use the food context to better understand the user's food preferences,
                    dish requirements, cuisine expectations, and relevant food information.

                    Do not invent restaurants, dishes, ratings, locations, or other details
                    that are not present in the provided contexts.

                    Explain briefly why each recommended restaurant matches the user's request.

                    Rank the recommendations from most suitable to least suitable.
                    """
                ),
                
                (
                    "human",
                    
                    """
                    User query:
                    {query}

                    Restaurant context:
                    {restaurant_context}

                    Food context:
                    {food_context}

                    Generate the best restaurant recommendations.
                    """
                    
                )
            ])
            
            self.recommendation_chain = self.prompt | self.llm
            
            
        except Exception:
            logger.exception("Error in recommendation agent init")
            raise
        
        
    async def run(self, query, restaurant_context, food_context):
        
        try:
            
            if not query:
                raise ValueError("query is missing")
            
            if not restaurant_context:
                raise ValueError("restaurant_context is missing")
                        
            if not food_context:
                food_context = "No additional food analysis available"
            
            response = await self.recommendation_chain.ainvoke({
                "query": query,
                "restaurant_context": restaurant_context,
                "food_context": food_context
            })
            
            return response
        
        except ValueError:
            logger.exception("Value error in recommendation agent run")
            raise

        except Exception:
            logger.exception("Error in recommendation agent run")
            raise