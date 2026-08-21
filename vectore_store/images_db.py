
from configurations.logger import get_logger
from documents_handler.image_recipe_data_handler import ImageRecipeHandler
from embeddings import embedding_handler


logger = get_logger("Image-vector-db")

class ImageVectorDB:
    
    def __init__(self, image_paths, recipe_data):
        
        try:
        
            self.image_paths = image_paths
            self.recipe_data = recipe_data
            self.embedding = embedding_handler
            self.image_handler = ImageRecipeHandler()
            
        except ValueError:
            logger.exception("Value error in image vector db")
            raise
        
        except Exception:
            logger.exception("Error in image vector db")
            raise
    
    def init_db(self):
        
        
        