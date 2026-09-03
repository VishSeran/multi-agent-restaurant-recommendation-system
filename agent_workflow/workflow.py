
from langgraph.graph import StateGraph
from langgraph.graph import START, END

from agent_workflow.workflow_state import WorkflowState
from agents.food_agent import FoodAgent
from agents.profile_agent import ProfileAgent
from agents.recommendation_agent import RecommendationAgent
from agents.relevance_evaluator_agent import RelevanceEvaluatorAgent
from configurations.logger import get_logger
from retriever.restaurant_retriever import RestaurantRetriever
from schema.recommendation_schema import RecommendationResponse
from schema.relevance_schema import RelevanceSchema
from vectore_store.images_db import ImageVectorDB
from vectore_store.restaurants_db import RestaurantVectorDB


logger = get_logger("workflow")

class MultiAgentWorkflow:
    
    def __init__(self, image_db, restaurant_db, retriever):
        
        self.profile_agent = ProfileAgent()
        self.relevance_agent = RelevanceEvaluatorAgent()
        self.food_agent = FoodAgent()
        self.recommendation_agent = RecommendationAgent()
        
        logger.info("Agents are initialized")
        
        self.image_db:ImageVectorDB = image_db
        self.restaurant_db:RestaurantVectorDB = restaurant_db
        self.retriever:RestaurantRetriever = retriever
        self.workflow =  None
        
        self.build_workflow()
        
    
    def build_workflow(self):
        
        try:
            
            graph = StateGraph(WorkflowState)
            graph.add_node("profile", self.profile_flow_node)
            graph.add_node("relevance_checker", self.relevance_checker_node)
            graph.add_node("rag_node",self.rag_node)
            graph.add_node("food_analyze", self.food_analyze_node)
            graph.add_node("recommendation_node", self.recommendation_node)

            graph.add_conditional_edges(START, self.profile_manager, {
                "relevance_checker": "relevance_checker",
                "profile": "profile"
            })
            
            graph.add_edge("profile", "relevance_checker")
            
            graph.add_conditional_edges("relevance_checker", self.relevancy_manager,{
                "rag_node": "rag_node",
                "end": END
            })
            graph.add_edge("rag_node", "food_analyze")
            graph.add_edge("food_analyze", "recommendation_node")
            graph.add_edge("recommendation_node", END)
            
            self.workflow = graph.compile()
            logger.info("Workflow compiled successfully")
            
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
            
            state['user_profile'] = profile
            return state
            
        except Exception:
            logger.exception("Error in profile agent flow")
            raise
        
        
    async def relevance_checker_node(self, state:WorkflowState):
            
            try:
                
                query = state['query']
                image_query = state['image_query']
                
                relevency_response:RelevanceSchema = await self.relevance_agent.relevancy_check(
                    query=query,
                    image_query=image_query
                )
                
                logger.info("Relevancy response is fetched")
                state['relevancy_response'] = relevency_response
                
                if relevency_response.relevancy in ("CAN_ANSWER", "PARTIAL"):
                    logger.info("Query is relevant to content")
                    state['relevance_result'] = "Query is relevant to the restaurant data"
                
                else:
                    logger.info("Query is relevant to content")
                    state['relevance_result'] = "Query is not relevant to restaurant data. please try with restaurant related query"
                    state['final_recommendation'] = [
                        {
                            "result": "Query is not relevant to restaurant data. please try with restaurant related query"
                        }
                    ]
                    
                
                return state
                
            except Exception:
                logger.exception("Error in relevance checker node")
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
            
            final_results:list[dict] = []
            
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
                
            content = []
                        
            for restaurant in final_results:
                for restaurant_id, data in restaurant.items():
                    text_content = "\n".join(
                        item['content']
                        for item in data['text_result']
                    )
                    
                    image_content = "\n".join(
                        item['metadata']
                        for item in data['image_result']
                    ) if isinstance(data['image_result'],list) else "No image description"
                    
                    restaurant_content = f"""
                            Restaurant ID: {restaurant_id}

                            Restaurant Details:
                            {text_content}

                            Image Details:
                            {image_content}
                            """
                    
                    content.append(restaurant_content)

            final_content = "\n\n".join(content)
            if final_content:
                logger.info("Final content is ready")
            
            state['retrieved_restaurants'] = final_results
            state['retrieved_content'] = final_content
            
            return state
            
            
        except Exception:
            logger.exception("Error in rag node")
            raise
    
   
    async def food_analyze_node(self, state: WorkflowState):
        
        try:
            retrieved_content = state.get("retrieved_content", "")
            response = await self.food_agent.run(retrieved_content)
            
            logger.info("Food analze response is fetched")
            state['food_analyst'] = response
            return state
            
        except Exception:
            logger.exception("Error in food analyze node")
            raise
        
    
    async def recommendation_node(self, state: WorkflowState):

        try:
            
            query = state.get("query", "")
            logger.info("query is fetched")
            
            restaurant_data = state.get("retrieved_restaurants", [])
            logger.info("restaurant data is fetched")
            
            food_context = state.get("food_analyst", "")
            logger.info("food context is fetched")
            
            recommendation_response:RecommendationResponse = await self.recommendation_agent.run(
                query=query,
                restaurant_context=restaurant_data,
                food_context=food_context
            )
            
            logger.info("recommendation is fetched")
            
            state['final_recommendation'] = [
                item.model_dump() 
                for item in recommendation_response.response
            ]
            
            logger.info("final recommendation state updated")
            return state

        except Exception:
            logger.exception("Error in recommendation process")
            raise
    
        
    def profile_manager(self, state:WorkflowState):
        
        try:
            
            profile_state = state.get("user_profile",{})
            
            if profile_state:
                logger.info("Existing user profile found")
                return "relevance_checker"
            
            logger.info("User profile missing")
            return "profile"
            
        except Exception:
            logger.exception("Error in profile manager")
            raise   
        
        
    def relevancy_manager(self, state:WorkflowState):
        
        try:
            relevancy:RelevanceSchema  = state['relevancy_response']
            
            if relevancy.relevancy in ["CAN_ANSWER", "PARTIAL"]:
                return "rag_node"
            
            else:
                return 'end'
 
        except Exception:
            logger.exception("Error in relevancy manager")
            raise
        
        
    
       
        
        