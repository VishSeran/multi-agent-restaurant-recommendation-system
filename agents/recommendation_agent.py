
from langchain_core.prompts import ChatPromptTemplate
from configurations.logger import get_logger
from llms.llm_handler import LLMHandler


logger = get_logger("recommendation-agent")

class RecommendationAgent:
    
    def __init__(self):
        
        try:
            
            self.llm_handler = LLMHandler(temperature=0.3)
            self.llm = self.llm_handler.get_llm()
            
            self.prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                     """
                    You are an expert restaurant recommendation agent.

                    Your task is to recommend the most suitable restaurants based on:
                    - The user's query and preferences
                    - Retrieved restaurant information
                    - Restaurant rankings and relevance scores
                    - Cuisine, location, rating, price range, and other available information

                    Only use the restaurant information provided in the context.
                    Do not invent restaurants or details that are not present in the context.

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
            
        except ValueError:
            logger.exception("Value error in recommendation agent run")
            raise

        except Exception:
            logger.exception("Error in recommendation agent run")
            raise