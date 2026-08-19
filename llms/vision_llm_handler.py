import os
from io import BytesIO
import base64
import httpx

from PIL import Image
import dotenv
from langchain_groq import ChatGroq

from configurations.configs import SYS_CAP_PROMPT, VISION_MODEL, USER_CAP_PROMPT, is_url
from configurations.logger import get_logger
from schema.image_caption import ImageCaptionSchema

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
            
            self.vision_structured_model = self.vision_model.with_structured_output(ImageCaptionSchema)
            
            logger.info("Vision model is initialized")
            
        except ValueError:
            logger.exception("Value Error in vision model")    
            
        except Exception:
            logger.exception("Error in vision model")
            
    
    async def img_to_data_url(self, img_path):
        
        try:
            
            if not img_path:
                raise ValueError("Image path is missing")
            

            if is_url(img_path):
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    
                    response = await client.get(img_path)
                    response.raise_for_status()
                    
                img_bytes = response.content
                content_type = response.headers.get("content-type", "image/jpeg")
                encoded_data = base64.b64encode(img_bytes).decode(encoding="utf-8")
   
            else:
                buffer = BytesIO()
                img = Image.open(img_path).convert("RGB")
                img.save(buffer,"JPEG")
                
                logger.info("image saved successfully in the buffer")
                
                content_type = "image/jpeg"
                encoded_data = base64.b64encode(buffer.getvalue()).decode(encoding="utf-8")
            
            return f"data:{content_type};base64,{encoded_data}" 

        except ValueError:
            logger.exception("Value error in get_vision_response")
            raise
        
        except Exception:
            logger.exception("Error in img to data url")
            raise    
    
            
    
    async def get_vision_response(self, img_data_url):
        
        try:
            
            if not img_data_url:
                raise ValueError("image data is missing")
            
            
            response = await self.vision_structured_model.ainvoke({
                
                "messages": [
                    {
                        "role": "system",
                        "content": SYS_CAP_PROMPT
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": USER_CAP_PROMPT
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": img_data_url
                                }
                            }
                        ]
                    }
                ]
            })
            
            logger.info("Response has fetched")
            return response
        
        except ValueError:
            logger.exception("Value error in get_vision_response")
            raise
            
        except Exception:
            logger.exception("Error in get_vision_response")
            raise
        
        
    
        
        
    
    