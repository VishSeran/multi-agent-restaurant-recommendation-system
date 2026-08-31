from langchain_core.prompts import ChatPromptTemplate

from configurations.logger import get_logger
from llms.llm_handler import LLMHandler
from schema.relevance_schema import RelevanceSchema
from vectore_store.images_db import ImageVectorDB
from vectore_store.restaurants_db import RestaurantVectorDB


logger = get_logger("relevance-evaluator-agent")

class RelevanceEvaluatorAgent:
    
    def __init__(self):
        
        
        self.llm_handler = LLMHandler(temperature=0.1)
        self.llm = self.llm_handler.get_llm().with_structured_output(RelevanceSchema)
        
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are an AI relevance checker between a user's question and provided document content.        
        
            Instructions:
            - Classify how well the document content addresses the user's question.
            - Respond with only one of the following labels: CAN_ANSWER, PARTIAL, NO_MATCH.
            - Do not include any additional text or explanation.        
            
            Labels:
            1) "CAN_ANSWER": The passages contain enough explicit information to fully answer the question.
            2) "PARTIAL": The passages mention or discuss the question's topic but do not provide all the details needed for a complete answer.
            3) "NO_MATCH": The passages do not discuss or mention the question's topic at all.        
            
            Important: If the passages mention or reference the topic or timeframe of the question in any way, even if incomplete, respond with "PARTIAL" instead of "NO_MATCH".        
            
            Question: {question}
            Passages: {question}        
            
            Respond ONLY with one of the following labels: CAN_ANSWER, PARTIAL, NO_MATCH"""
            ),
            
            (
                "human",
                """
                Question: {question}
                
                document_content: {document_content}
                 
                """
            )
        ])
        
        self.relevance_chain = self.prompt | self.llm
        logger.info("relevance chain is created")
    
        
    async def relevancy_check(self, 
                            query:str, 
                            image_query:str|None,
                            image_db:ImageVectorDB,
                            restaurant_db: RestaurantVectorDB):
        
        try:
            
            if not query:
                raise ValueError("Query is missing")
            
            top_text_docs:list[dict] = await restaurant_db.search_query(query) 
            
            doc_content = []
            for item in top_text_docs:
                content = item.get("content", "")
                
                if content:
                    doc_content.append(content)
                
            if image_query:
                top_image_docs:list[dict] = await image_db.image_query_search(image_query)
                
                for item in top_image_docs:
                    metadata = item.get("metadata", {})
                    cuisine = metadata.get("cuisine", "")
                    
                    if cuisine:
                        doc_content.append(f"Image cuisine information: {cuisine}")
                    
            logger.info("relevant docs are retrieved")
            final_content = "\n\n".join(doc_content)
                    
            
            response = await self.relevance_chain.ainvoke({
                "question": query,
                "document_content": final_content
            })
            
            response = response.model_dump()
            logger.info("Relevancy response is fetched")
            
            return response
            
        except ValueError:
            logger.exception("Value error in relevancy check")
            raise
        
        except Exception:
            logger.exception("Error in relevancy check")
            raise 