from langchain_core.documents import Document

from configurations.logger import get_logger


logger = get_logger("image-recipe-data-handler")

class ImageRecipeHandler:
    
    def __init__(self):
        pass
    
    def __call__(self, image_path, recipe_data):
        
        try:
            
            if not image_path:
                raise ValueError("Image path is missing")
            
            for i, (img, recipe) in enumerate(zip(image_path, recipe_data)):
                
                doc_id = f"doc_{i}"
                
                
            
            
            
        except Exception:
            logger.exception("Error in ImageRecipeHandler")
            raise
    
    