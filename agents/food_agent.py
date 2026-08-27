
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
                
                            You are a food specialist agent.

                        Analyze the user's request and decide which available
                        food tools are required.

                        Available capabilities:

                        1. food_analysis_tool
                        Use for questions about ingredients, taste,
                        preparation, dishes, or food characteristics.

                        2. food_style_tool
                        Use when determining cuisine, food category,
                        culinary style, or regional style.

                        3. nutrition_analysis_tool
                        Use for questions about nutrition, calories,
                        protein, carbohydrates, fats, or dietary values.

                        You may call one or multiple tools depending on
                        the user's request.

                        Do not call tools that are irrelevant.
            
                """
            )
             
            
        except Exception:
            logger.exception("Error in food agent")
            raise
        
        
        async def run(self, query):
            
            try:
                
                if not query:
                    raise ValueError("Query is missing")
                
            
            
            except ValueError:
                logger.exception("Value error in food agent run")
                raise    
            
            except Exception:
                logger.exception("Error in food agent run")
                raise