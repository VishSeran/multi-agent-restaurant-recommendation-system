
from langchain_huggingface import HuggingFaceEmbeddings
from configurations.logger import get_logger

from configurations.configs import TEXT_EMBEDDING_MODEL,IMAGE_EMBEDDING_MODEL

logger = get_logger("embedding-handler")

class EmbeddingHandler:
    
    def __init__(self, 
                 text_embed_model = TEXT_EMBEDDING_MODEL, 
                 img_embed_model = IMAGE_EMBEDDING_MODEL ):
        
        try:
            
            if not text_embed_model:
                raise ValueError("text embedding model is missing")
            
            if not img_embed_model:
                raise ValueError("image embedding model is missing")
        
            self.text_embedding_model = HuggingFaceEmbeddings(
                model_name = text_embed_model 
            )
            self.image_embedding_model = None
        
        except ValueError:
            logger.exception("Value error in embedding handler init")
            raise
        
        except Exception:
            logger.exception("Error in embedding handler init")
            raise
    