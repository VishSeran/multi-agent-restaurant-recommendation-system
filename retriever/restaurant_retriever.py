

from configurations.logger import get_logger


logger = get_logger("restaurant_retriever")

class RestaurantRetriever:
    
    def __init__(self, text_retriever, image_retriever, reranker):
        
        self.text_retriever = text_retriever,
        self.image_retriever = image_retriever,
        self.reranker = reranker