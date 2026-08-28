
from langgraph.graph import StateGraph

from agent_workflow.workflow_state import WorkflowState
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
            
            graph = StateGraph(WorkflowState)
            
        except Exception:
            logger.exception("Error in build workflow")
            raise
        
    
        
        
    
        
        
       
        
        