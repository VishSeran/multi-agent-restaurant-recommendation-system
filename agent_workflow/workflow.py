
from langgraph.graph import StateGraph

from agent_workflow.workflow_state import WorkflowState
from agents.food_agent import FoodAgent
from agents.profile_agent import ProfileAgent
from agents.recommendation_agent import RecommendationAgent
from configurations.logger import get_logger
from retriever.restaurant_retriever import RestaurantRetriever
from vectore_store.images_db import ImageVectorDB
from vectore_store.restaurants_db import RestaurantVectorDB


logger = get_logger("workflow")

class MultiAgentWorkflow:
    
    def __init__(self, image_db, restaurant_db, retriever):
        
        self.profile_agent = ProfileAgent()
        self.food_agent = FoodAgent()
        self.recommendation_agent = RecommendationAgent()
        
        logger.info("Agents are initialized")
        
        self.image_db:ImageVectorDB = image_db
        self.restaurant_db:RestaurantVectorDB = restaurant_db
        self.retriever:RestaurantRetriever = retriever
        
        self.build_workflow()
        
    
    def build_workflow(self):
        
        try:
            
            graph = StateGraph(WorkflowState)
            graph.add_node("profile", self.profile_flow_node)
            graph.add_node("rag_node",self.rag_node)
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
        
        
    async def rag_node(self, state:WorkflowState):
        
        try:
            
            query = state.get("query", "")
            image_query = state.get("image_query", "")
            
            text_results = []
            image_results = []
            if query:
                text_results = await self.restaurant_db.search_query(
                    query=query
                )
            
            if image_query:
                image_results = await self.image_db.image_query_search(
                    image_query=image_query
                )

            self.retriever.fuse_result(
                text_results=text_results,
                image_results=image_results
            )
            
            final_retrieved_list = self.retriever.reranker(query)
            
            final_results = []
            
            for item in final_retrieved_list:
                
                final_results.append({
                    
                   item['restaurant_id']: {
                    
                    "text_result": item['text_results'],
                    "image_result": (item['image_results'] if item['image_results'] 
                                    else "No image decription"),
                    "fusion_score": item['fusion_score'],
                    "rerank_score": item['rerank_score']
                
                    }}
                ) 
                
            return {
                "retrieved_restaurants":final_results
            }
            
            
        except Exception:
            logger.exception("Error in rag node")
            raise
        
        
    async def food_analyze_node(self, state: WorkflowState):
        
        try:
            restaurants_data = state.get("retrieved_restaurants", "")
            
            content = "\n\n".join(
               ( f"""
                    Restuarant ID: {restaurant_id}
                    Text Details: {"\n\n".join(
                        item for item in data['text_result']
                    )}
                    Image Details: {"\n\n".join(
                        item for item in data['image_result']
                    )}
                """
                
                for restaurant_id, data in restaurant.items()) for restaurant in restaurants_data
            )
            
            response = await self.food_agent.run(content)
            
            return {
                "food_analyst": response
            }
            
        except Exception:
            logger.exception("Error in food analyze node")
            raise
        
    
        
    
        
        
    
        
        
       
        
        