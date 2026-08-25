
from configurations.logger import get_logger


logger = get_logger("reranker")

class ReRanker:
    
    def __init__(self):
        
        self.reranker = 