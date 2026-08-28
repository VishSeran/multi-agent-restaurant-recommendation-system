
from langgraph.prebuilt import 

from agents.profile_agent import ProfileAgent
from configurations.logger import get_logger


logger = get_logger("workflow")

class MultiAgentWorkflow:
    
    def __init__(self):
        
        self.profile_agent = ProfileAgent()
        self.food_agent 
        
        