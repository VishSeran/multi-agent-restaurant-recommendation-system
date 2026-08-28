
from langchain.agents import create_agent

from agent_tools.food_agent_tools import food_analyze, food_style_analyze, nutrition_analze
from configurations.logger import get_logger
from llms.llm_handler import LLMHandler


logger = get_logger("food-agent")


class FoodAgent:
    
    def __init__(self):
        
        
        try:
            
            self.llm_handler = LLMHandler(temperature=0.4)
            self.chat_llm = self.llm_handler.get_llm()
            
            logger.info("Chat LLM initiated")
            
            self.food_agent = create_agent(
                model=self.chat_llm,
                tools=[food_analyze, food_style_analyze, nutrition_analze],
                system_prompt="""
                    You are a food specialist agent supporting a restaurant recommendation system.

                    Analyze the user's request and extract food-related information that can help
                    another agent recommend suitable restaurants.

                    Available capabilities:

                    1. food_analysis_tool
                    Use for ingredients, taste, preparation methods, dishes,
                    and food characteristics.

                    2. food_style_tool
                    Use for cuisine, food category, culinary style,
                    and regional food styles.

                    3. nutrition_analysis_tool
                    Use for nutrition, calories, protein, carbohydrates,
                    fats, and dietary values.

                    You may call one or multiple tools when necessary.

                    Do not call irrelevant tools.

                    Your final response should summarize only the food-related information
                    that is useful for restaurant recommendation.
                    """
            )
            logger.info("food agent is created")
             
            
        except Exception:
            logger.exception("Error in food agent")
            raise
        
        
    async def run(self, query):
        
        try:
            
            if not query:
                raise ValueError("Query is missing")
            
            response = await self.food_agent.ainvoke({
                "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            })
            
            logger.info("food agent response is fetched")
            return response['messages'][-1].content
        
        except ValueError:
            logger.exception("Value error in food agent run")
            raise    
        
        except Exception:
            logger.exception("Error in food agent run")
            raise