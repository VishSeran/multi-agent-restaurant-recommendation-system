
from configurations.logger import get_logger
from documents_handler.image_recipe_data_handler import ImageRecipeHandler
from embeddings.embedding_handler import embedding_handler


logger = get_logger("Image-vector-db")

class ImageVectorDB:
    
    def __init__(self, image_paths, recipe_data):
        
        try:
            
            if not image_paths:
                raise ValueError("Image paths are missing")
            
            if not recipe_data:
                raise ValueError("Recipe data is missing")

            self.vector_db = None
            self.image_paths = image_paths
            self.recipe_data = recipe_data
            self.image_handler = ImageRecipeHandler()
            
        except ValueError:
            logger.exception("Value error in image vector db")
            raise
        
        except Exception:
            logger.exception("Error in image vector db")
            raise
    
    def init_db(self):
        
        
        try:
            
            image_docs_list = self.image_handler(self.image_paths, self.recipe_data)
            image_embeddings = embedding_handler.get_image_embeddings([
                doc.metadata.get("image_path") for doc in image_docs_list
            ])
            
            
            
        except ValueError:
            logger.exception("Value error in init db")
            raise
        
        except Exception:
            logger.exception("Error in init db")
            raise