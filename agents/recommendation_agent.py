

from configurations.logger import get_logger
from llms.llm_handler import LLMHandler


logger = get_logger("recommendation-agent")

class RecommendationAgent:
    
    def __init__(self):
        
        try:
            
            self.llm_handler = LLMHandler(temperature=0.3)
            self.llm = self.llm_handler.get_llm()
            
            
            
        except Exception:
            logger.exception("Error in recommendation agent init")
            raise