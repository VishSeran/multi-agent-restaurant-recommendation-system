from langchain_chroma.vectorstores import Chroma

from configurations.configs import DB_DIR
from configurations.logger import get_logger
from embeddings import embedding_handler


logger =  get_logger("restaurant-db")

class RestaurantVectorDB:
    
    def __init__(self):
        
        self.vector_store = Chroma(
            collection_name="restaurants_data",
            persist_directory=DB_DIR
        )
        logger.info("Restaurant chroma db initiated")
        
        self.embedding = embedding_handler
        
        
    def create_restaurant_vector_store():
        
        try:
            