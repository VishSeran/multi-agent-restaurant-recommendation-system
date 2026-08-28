
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
            graph.add_node("profile", self.profile_flow_node)
            graph.add_node("food_analyze", self.food_analyze_node)
            
        except Exception:
            logger.exception("Error in build workflow")
            raise
        
        
    async def profile_flow_node(self, state: WorkflowState):
        
        try:
            
            user_id = state.get("user_id","")
            review_history = state.get("user_reviews","")
            
            response = await self.profile_agent.generate_profile(
                user_id=user_id,
                review_history=review_history
            ) 
            
            profile = response.model_dump()
            logger.info(f"{profile['user_id']} profile updated")
            
            return {
                "user_profile": profile
            }
            
        except Exception:
            logger.exception("Error in profile agent flow")
            raise
        
        
    async def food_analyze_node(self, state: WorkflowState):
        
        try:
            
            user_query = state.get("query","")
            
        except Exception:
            logger.exception("Error in food analyze node")
            raise
        
    
        
    
        
        
    
        
        
       
        
        