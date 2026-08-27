
from retriever.reranker import reranker_obj
from configurations.logger import get_logger


logger = get_logger("restaurant_retriever")

class RestaurantRetriever:
    
    def __init__(self, query,text_retriever, image_retriever):
        
        self.text_retriever = text_retriever
        self.image_retriever = image_retriever
        self.query = query
        self.re_ranker = reranker_obj.get_reranker()
        self.sorted_list = None
        self.final_sort_list = None
        
    def reciprocal_score(self,rank:int, constant:int = 60):
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
                fuse[restaurant_id]['text_results'].append(item)
                
                
            for item in image_results:
                restaurant_id = item.get('doc_id', '')
                
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
                
            
            self.sorted_list = sorted(
                fuse.values(),
                key= lambda x: x['fusion_score'],
                reverse=True
            )
            
            return self.sorted_list

        except Exception:
            logger.exception("Error in fuse result")
            raise
        
    
    def reranker(self):
        
        try:
            
            sorted_list = self.sorted_list[:15]
            
            if not self.sorted_list:
                return []
            
            reranker_pairs = []
            
            for candidate in sorted_list:
                
                content = []
                
                for item in candidate['text_results']:
                    content.append(item['content'])
                    
                for item in candidate['image_results']:
                    content.append(
                        f"Image description: {item['content']}"
                    )
                    
                combined_text = "\n".join(content)
                
                reranker_pairs.append([
                    self.query,
                    combined_text
                ])
            
            scores = self.re_ranker.compute_score(reranker_pairs, normalize = True)
        
            for item, score in zip(sorted_list, scores):
                item['rerank_score'] = float(score)
                
            self.final_sort_list =  sorted(
                sorted_list,
                key= lambda x: x["rerank_score"],
                reverse=True
            )
            
            return self.final_sort_list[:5]
           
        except Exception:
            logger.exception("Error in reranker")
            raise