

from configurations.logger import get_logger


logger = get_logger("restaurant_retriever")

class RestaurantRetriever:
    
    def __init__(self, text_retriever, image_retriever):
        
        self.text_retriever = text_retriever,
        self.image_retriever = image_retriever,
        
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
                fuse[restaurant_id]['fusion_score'] += score
                fuse[restaurant_id]['text_result'].append(item)
                
                
            for item in image_results:
                restaurant_id = item.get['doc_id']
                
                if restaurant_id not in fuse:
                    fuse[restaurant_id] = {
                        "restaurant_id": restaurant_id,
                        "fusion_score": 0.0,
                        "text_results": [],
                        "image_results": []
                    }    
                    
                score = image_weight * self.reciprocal_score(item['rank'])
                fuse[restaurant_id]['fusion_score'] += score
                fuse[restaurant_id]['image_results'].append(item)
                
            
            sort = sorted(
                fuse.values(),
                key= lambda x: x['fusion_score'],
                reverse=True
            )
            
            return sort

        except Exception:
            logger.exception("Error in fuse result")
            raise
        
    
    def reranker(self, sorted_list: list[dict]):
        
        try:
            
            text_combination = []
            
            for item in sorted_list['text_results']:
                text_combination.append(item['content'])
                
            for item in sorted_list['image_results']:
                text_combination.append(f"Image description: {item['content']}")
                
            return "\n".join(text_combination)
            
            
        except Exception:
            logger.exception("Error in reranker")
            raise