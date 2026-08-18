import os
import dotenv
from langchain_groq import ChatGroq

from configurations.configs import VISION_MODEL
from configurations.logger import get_logger


logger = get_logger("vision-llm")
dotenv.load_dotenv()

class VisionLLMHandler:
    
    def __init__(self, vision_model = VISION_MODEL):
        
        try:
            
            groq_api = os.getenv("GROQ_API")
            
            if not groq_api:
                raise ValueError("Error in groq api")
            
            self.vision_model = ChatGroq(
                model=vision_model,
                api_key=groq_api,
                temperature=0.4,
                max_tokens=4000,
                verbose=True
            )
            
            logger.info("Vision model is initialized")
            
        except ValueError:
            logger.exception("Value Error in vision model")    
            
        except Exception:
            logger.exception("Error in vision model")