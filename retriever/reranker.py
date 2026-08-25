from FlagEmbedding import FlagReranker
from configurations.logger import get_logger


logger = get_logger("reranker")

class ReRanker:
    
    def __init__(self):
        
        self.reranker = FlagReranker(
            "BAAI/bge-reranker-v2-m3",
            use_fp16=True
        )
        
        logger.info("reranker initited")
        
        
    def get_reranker(self):
        return self.reranker
    
    
reranker_obj = ReRanker()