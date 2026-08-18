
from configurations.configs import VISION_MODEL
from configurations.logger import get_logger


logger = get_logger("vision-llm")

class VisionLLMHandler:
    
    def __init__(self, vision_model = VISION_MODEL):
        
        try:
            
        except Exception:
            logger.exception("Error in vision model")