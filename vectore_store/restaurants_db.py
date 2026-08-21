from langchain_chroma.vectorstores import Chroma

from configurations.configs import DB_DIR
from configurations.logger import get_logger


logger =  get_logger("restaurant-db")

class RestaurantVectorDB:
    
    def __init__(self):
        
        self.vector_store = Chroma(
            collection_name="restaurants_data",
            persist_directory=DB_DIR
        )
        logger.info("Restaurant chroma db initiated")