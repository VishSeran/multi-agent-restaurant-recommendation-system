
from configurations.logger import get_logger
from langchain_core.documents import Document

logger = get_logger("document-handler")

class RestaurantsDataHandler:
    
    def __init__(self):
        
        pass
        
    def __call__(self, restaurants_data):
        
        try:
            
        except Exception:
            logger.exception("Error in restaurants data handler")
            raise