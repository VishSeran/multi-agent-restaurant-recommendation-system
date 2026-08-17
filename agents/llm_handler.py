import os
import dotenv

from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

from configurations.configs import GROQ_MODEL
from configurations.logger import get_logger


logger = get_logger("llm-handler")
dotenv.load_dotenv()
class LLMHandler:
    
    def __init__(self):
        
        try:
            self.model_name = GROQ_MODEL
            
            API = os.getenv("GROQ_API")
            
            if not API:
                raise ValueError("Groq api key is missing")

            self.configs = {
                "configurables": {
                    "thread_id": "conversational_id"
                }
            }
            
            self.chat_groq = ChatGroq(
                model=self.model_name,
                api_key=API,
                max_tokens=5000,
                verbose=True
            )
            
            logger.info("Chat groq is created")
        
        except Exception:
            logger.exception("Error in llm handler")
            raise