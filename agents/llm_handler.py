
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

from configurations.configs import GROQ_MODEL
from configurations.logger import get_logger


logger = get_logger("llm-handler")

class LLMHandler:
    
    def __init__(self):
        
        self.model_name = GROQ_MODEL
        
        self.configs = {
            "configurables": {
                "thread_id": "conversational_id"
            }
        }
        
        checkpointer = 
        self.chat_groq