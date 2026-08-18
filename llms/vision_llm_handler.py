import os

from PIL import Image
import dotenv
from langchain_groq import ChatGroq

from configurations.configs import SYS_CAP_PROMPT, VISION_MODEL
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
            
    
    def img_to_data_url(self, img_path):
        
        try:
            
            if not img_path:
                raise ValueError("Image path is missing")
            
            
        
        except Exception:
            logger.exception("Error in img to data url")
            raise    
    
            
    
    async def get_vision_response(self, img_path):
        
        try:
            
            if not img_path:
                raise ValueError("image data is missing")
            
            
            response = await self.vision_model.ainvoke({
                "messages": [
                    {
                        "role": "system",
                        "content": SYS_CAP_PROMPT
                    },
                    {
                        "role": "user",
                        "content": img_path
                    }
                ]
            })
        
        except ValueError:
            logger.exception("Value error in get_vision_response")
            raise
            
        except Exception:
            logger.exception("Error in get_vision_response")
            raise
        
        
    
    