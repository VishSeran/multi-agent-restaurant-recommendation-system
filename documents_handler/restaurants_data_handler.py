
from configurations.configs import Base_dir
from configurations.logger import get_logger
from langchain_core.documents import Document


logger = get_logger("document-handler")

class RestaurantsDataHandler:
    
    def __init__(self):
        
        self.file_name = Base_dir / "dataset" / "restaurants" / "structured_restaurant_data.json"
        
    def __call__(self, restaurants_data:list[dict]):
        
        try:
            
            restaurants_docs = []
            
            for i, restaurant in enumerate(restaurants_data):
                name = str(restaurant.get("name", "")).strip()
                
                texts = (
                    f"Restaurant: {name}\n"
                    f"Cuisine: {restaurant.get("food_style", "")}\n"
                    f"Location: {restaurant.get("location", "")}"
                )
                
                doc_id = f"res_{i}"
                
                restaurants_docs.append(
                    Document(
                        page_content= texts.strip(),
                        metadata = {
                            "doc_id": doc_id,
                            "cuisine": restaurant.get("food_style"),
                            "location": restaurant.get("location"),
                            "source": self.file_name
                        }
                    )
                )
            
            logger.info("restaurant data successfully documentarized")
            return restaurants_docs 
            
        except Exception:
            logger.exception("Error in restaurants data handler")
            raise
        
        
    