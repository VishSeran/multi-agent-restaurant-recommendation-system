import torch
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import CLIPModel, CLIPProcessor

from configurations.logger import get_logger

from configurations.configs import TEXT_EMBEDDING_MODEL,IMAGE_EMBEDDING_MODEL, Base_dir

logger = get_logger("embedding-handler")


CACHE_DIR = Base_dir / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class EmbeddingHandler:
    
    def __init__(self, 
                text_embed_model = TEXT_EMBEDDING_MODEL, 
                img_embed_model = IMAGE_EMBEDDING_MODEL ):
        
        try:
            
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Device is initiated: {device}")
            
            if not text_embed_model:
                raise ValueError("text embedding model is missing")
            
            if not img_embed_model:
                raise ValueError("image embedding model is missing")
        
            self.text_embedding_model = HuggingFaceEmbeddings(
                model_name = text_embed_model,
                model_kwargs = {
                    "device": device
                },
                encode_kwargs = {
                    "normalize_embeddings": True
                }
            )
            
            logger.info("text embedding model is initiated")
            
            self.image_embedding_model = CLIPModel.from_pretrained(
                img_embed_model,
                cache_dir=CACHE_DIR
            ).to(device)
            
            self.image_processor = CLIPProcessor.from_pretrained(
                img_embed_model,
                cache_dir=CACHE_DIR
            ) 
            
            logger.info("Image embedding model is initiated")
        
        except ValueError:
            logger.exception("Value error in embedding handler init")
            raise
        
        except Exception:
            logger.exception("Error in embedding handler init")
            raise
        
        
    def get_image_embeddings(self, image_path):
        
        try:
            
            if not image_path:
                raise ValueError("Image path is missing")
            
        except ValueError:
            logger.exception("Value error in get_image_embeddings")
            raise
        
        except Exception:
            logger.exception("Error in get_image_embeddings")
            raise
        
        
    