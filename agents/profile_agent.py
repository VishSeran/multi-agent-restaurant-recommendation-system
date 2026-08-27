
from langchain_groq import ChatGroq
from configurations.configs import GROQ_MODEL
from configurations.logger import get_logger


logger = get_logger("profile-agent")

class ProfileAgent:
    
    def __init__(self, model_name=GROQ_MODEL):
        
        
        self.groq_chain = ChatGroq(
            model=model_name,
            temperature=0.1,
            api_key=groq_api
            
        )
        