

from configurations.logger import get_logger


logger = get_logger("restaurant_retriever")

class RestaurantRetriever:
    
    def __init__(self, text_retriever, image_retriever, reranker):
        
        self.text_retriever = text_retriever,
        self.image_retriever = image_retriever,
        self.reranker = reranker
        
    def reciprocal_score(rank:int, constant:int = 60):
        return 1/ (rank+constant)
    
    
    
    def fuse_result(
        self,
        text_results: list[dict],
        image_results: list[dict],
        text_weight:float = 0.7,
        image_weight:float = 0.3
    ):
        
        try:
            
            fuse = {}
            
            for item in text_results:
                restaurant_id = item.get("doc_id","")
                
                if restaurant_id not in fuse:
                
                    fuse[restaurant_id] = {
                        "restaurant_id": restaurant_id,
                        "fusion_score": 0.0,
                        "text_results": [],
                        "image_results": []
                    }
                    
                score = text_weight * self.reciprocal_score(item["rank"])
                fuse[restaurant_id]['fusion_score'] = score
                fuse[restaurant_id]['text_result'].append(item)
                
                
                
            
            
            
            
        except Exception:
            logger.exception("Error in fuse result")
            raise