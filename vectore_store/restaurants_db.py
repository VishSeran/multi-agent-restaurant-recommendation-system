from langchain_chroma.vectorstores import Chroma

from configurations.configs import DB_DIR
from configurations.logger import get_logger
from documents_handler.restaurants_data_handler import RestaurantsDataHandler
from embeddings.embedding_handler import embedding_handler


logger =  get_logger("restaurant-db")

class RestaurantVectorDB:
    
    def __init__(self, restaurants_data):

        self.restaurants_data = restaurants_data
        self.restaurant_handler = RestaurantsDataHandler()
        
        self.embedding = embedding_handler
        
        self.vector_store = Chroma(
                    collection_name="restaurants_articles",
                    persist_directory=DB_DIR,
                    embedding_function=self.embedding.get_text_embedding_model()
                )
        
        self.restaurant_store_retriever = None
        
        logger.info("Restaurant chroma db initiated")
        
        
    def create_restaurant_vector_store(self):
        
        try:
            
            if self.vector_store is None:
                raise RuntimeError("Please initial restaurants chroma db first")
            
            restaurant_documents = self.restaurant_handler(self.restaurants_data)
            
            self.vector_store.add_documents(
                documents=restaurant_documents,
                ids=[doc.metadata['doc_id'] for doc in restaurant_documents]
            )
            
            logger.info("Restaurant chroma db ready!!!")
            
            self.restaurant_store_retriever = self.vector_store.as_retriever(
                search_type = "mmr",
                search_kwargs = {
                    "k": 6
                }
            )
            
            logger.info("Restaurant chroma db retriever ready!!!")
            
        except Exception:
            logger.exception("Error in create_restaurant_vector_store")
            raise
        
    
        
    
    def search_query(query:str):
        
        try:
            
            if not query:
                raise ValueError("query is missing")
            
            
            
        except ValueError:
            logger.exception("Value error in search query")
            raise
        
        except Exception:
            logger.exception("Error in search query")
            raise