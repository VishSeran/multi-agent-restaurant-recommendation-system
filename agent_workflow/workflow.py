
from langgraph.prebuilt import 

from agents.food_agent import FoodAgent
from agents.profile_agent import ProfileAgent
from agents.recommendation_agent import RecommendationAgent
from configurations.logger import get_logger


logger = get_logger("workflow")

class MultiAgentWorkflow:
    
    def __init__(self):
        
        self.profile_agent = ProfileAgent()
        self.food_agent = FoodAgent()
        self.recommendation_agent = RecommendationAgent()
        
        logger.info("Agents are initialized")
        
        self.build_workflow()
        
    
    def build_workflow(self):
        
        try:
            
            
            
        except Exception:
            logger.exception("Error in build workflow")
            raise
        
    
        
        
    
        
        
       
        
        