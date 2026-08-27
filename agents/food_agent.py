

from configurations.logger import get_logger
from llms.llm_handler import LLMHandler


logger = get_logger("food-agent")


class FoodAgent:
    
    def __init__(self):
        
        
        try:
            
            self.llm_handler = LLMHandler(temperature=0.4)
            self.chat_llm = self.llm_handler.get_llm()
            
            logger.info("Chat LLM initiated")
            
             
            
        except Exception:
            logger.exception("Error in food agent")
            raise