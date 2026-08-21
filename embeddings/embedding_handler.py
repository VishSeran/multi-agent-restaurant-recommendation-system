import numpy as np
import torch
from pathlib import Path
from PIL import Image
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
            
            self.IMAGE_EXTENSIONS = {
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".webp",
                }
            
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Device is initiated: {self.device}")
            
            if not text_embed_model:
                raise ValueError("text embedding model is missing")
            
            if not img_embed_model:
                raise ValueError("image embedding model is missing")
        
            self.text_embedding_model = HuggingFaceEmbeddings(
                model_name = text_embed_model,
                model_kwargs = {
                    "device": self.device
                },
                encode_kwargs = {
                    "normalize_embeddings": True
                }
            )
            
            logger.info("text embedding model is initiated")
            
            self.image_embedding_model = CLIPModel.from_pretrained(
                img_embed_model,
                cache_dir=CACHE_DIR
            ).to(self.device)
            
            self.image_processor = CLIPProcessor.from_pretrained(
                img_embed_model,
                cache_dir=CACHE_DIR
            ) 
            
            self.image_embedding_model.eval()
            
            logger.info("Image embedding model is initiated")
        
        except ValueError:
            logger.exception("Value error in embedding handler init")
            raise
        
        except Exception:
            logger.exception("Error in embedding handler init")
            raise
        
    
    @torch.inference_mode()  
    def get_image_embeddings(self, image_path: Path | list[Path],
                            batch_size = 16):
        
        try:
            
            if not image_path:
                raise ValueError("Image path is missing")
            
            vectors = []
            
            
            
            if image_path.exists():
                
                if image_path.is_file():
                    images = []
                    with Image.open(image_path) as image:
                        image = image.convert("RGB")
                        images.append(image)
                        
                elif image_path.is_dir():
                    
                    paths = [
                        path 
                        for path in image_path.iterdir()
                        if path.is_file()
                        and path.suffix.lower() in self.IMAGE_EXTENSIONS
                    ]
                                
                    
                    for i in range(0, len(paths), batch_size):
                        
                        images = []
                        
                        batch = paths[i : i+batch_size]
                        
                        for path in batch:
                            with Image.open(path) as img:
                                images.append(img.convert("RGB"))
                                
            
                        inputs = self.image_processor(
                            images=images,
                            return_tensors = "pt"
                        )
                    
                        inputs = {
                            key: value.to(self.device)
                            for key, value in inputs.items()
                        }
                    
                        features = self.image_embedding_model.get_image_features(**inputs)
                    
                        # L2 normalization for cosine similarity
                        features = torch.nn.functional.normalize(
                            features,
                            p=2,
                            dim=-1
                        )
                    
                        vectors.append(features.cpu().numpy().astype(np.float32))
                        logger.info("image vectors are updated")
                    
                else:
                    raise RuntimeError(f"Error in file type: {image_path}")
            
            else:
                raise FileNotFoundError(f"File not found in {image_path}")
            
            if not vectors:
                return np.empty(
                    (0, self.image_embedding_model.config.projection_dim),
                    dtype=np.float32
                )
            
            logger.info("Vectors are concatenated")   
            return np.concatenate(vectors, axis=0)
            
        except ValueError:
            logger.exception("Value error in get_image_embeddings")
            raise
        
        except Exception:
            logger.exception("Error in get_image_embeddings")
            raise
    
    def get_text_embeddings(self,text:list[str]):
        
        try:
            if not text:
                raise ValueError("Texts are missing")
            
            embeddings = self.text_embedding_model.embed_documents(text)
            return np.ndarray(
                embeddings,
                dtype=np.float32
            )

        except Exception:
            logger.exception("Error in get text embeddings")
            raise
        
embedding_handler = EmbeddingHandler()