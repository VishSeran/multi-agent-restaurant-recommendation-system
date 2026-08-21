from langchain_core.documents import Document

from configurations.configs import Base_dir
from configurations.logger import get_logger


logger = get_logger("image-recipe-data-handler")

class ImageRecipeHandler:
    
    def __init__(self):
        self.filename = Base_dir / "dataset" / "restaurants" / "augmented_food_recipe.json"
    
    def __call__(self, image_path, recipe_data:list[dict]):
        
        try:
            
            if not image_path:
                raise ValueError("Image path is missing")
            
            image_docs = []
            
            for i, (img, recipe) in enumerate(zip(image_path, recipe_data)):
                
                doc_id = f"doc_{i}"
                
                image_docs.append(
                    Document(
                        page_content= recipe.get("name", f"recipe image {i}"),
                        metadata = {
                            "doc_id": doc_id,
                            "image_path": img,
                            "recipe_id" : recipe.get("id"),
                            "cuisine": recipe.get("cuisine"),
                            "source": self.filename
                        }
                    )
                )
                
            
            
            
        except Exception:
            logger.exception("Error in ImageRecipeHandler")
            raise
    
    