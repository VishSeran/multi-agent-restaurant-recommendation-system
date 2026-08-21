from langchain_chroma.vectorstores import Chroma

from configurations.configs import DB_DIR
from configurations.logger import get_logger
from embeddings import embedding_handler


logger =  get_logger("restaurant-db")

class RestaurantVectorDB:
    
    def __init__(self, restaurants_data):
        
        self.vector_store = Chroma(
            collection_name="restaurants_data",
            persist_directory=DB_DIR
        )
        logger.info("Restaurant chroma db initiated")
        self.restaurants_data = restaurants_data
        
        self.embedding = embedding_handler
        
        
    def create_restaurant_vector_store(self):
        
        try:
            
            if self.vector_store is None:
                raise RuntimeError("Please initial restaurants chroma db first")
            
            self.vector_store.from_documents(
                documents=self.restaurants_data,
                embedding=self.embedding.
            )
        except Exception:
            logger.exception("Error in create_restaurant_vector_store")
            raise