from langchain_chroma.vectorstores import Chroma
from configurations.configs import DB_DIR
from configurations.logger import get_logger
from documents_handler.image_recipe_data_handler import ImageRecipeHandler
from embeddings.embedding_handler import embedding_handler


logger = get_logger("Image-vector-db")

class ImageVectorDB:
    
    def __init__(self, image_paths, recipe_data):
        
        try:
            
            if not image_paths:
                raise ValueError("Image paths are missing")
            
            if not recipe_data:
                raise ValueError("Recipe data is missing")

            self.vector_db = Chroma(
                        collection_name="food_images",
                        persist_directory= DB_DIR,
                    ) 
            
            logger.info("food_images chroma db created")
                   
            self.image_paths = image_paths
            self.recipe_data = recipe_data
            self.image_handler = ImageRecipeHandler()
            
        except ValueError:
            logger.exception("Value error in image vector db")
            raise
        
        except Exception:
            logger.exception("Error in image vector db")
            raise
    
    def create_food_image_vector_store(self):
        
        
        try:
            
            image_docs_list = self.image_handler(self.image_paths, self.recipe_data)
            image_embeddings = embedding_handler.get_image_embeddings([
                doc.metadata.get("image_path") for doc in image_docs_list
            ])
            
            image_embeddings = image_embeddings.tolist()
            
            if self.vector_db is None:
                raise RuntimeError("Please create image chroma db first")
            
            self.vector_db._collection.upsert(
                ids=[doc.metadata['doc_id'] for doc in image_docs_list],
                embeddings=image_embeddings,
                metadatas=[doc.metadata for doc in image_docs_list],
                documents=[doc.page_content for doc in image_docs_list]
            )
            
            logger.info("Food image db ready!!!")
            
            
        except ValueError:
            logger.exception("Value error in init db")
            raise
        
        except Exception:
            logger.exception("Error in init db")
            raise
        
        
    def image_query_search(self,image_query,where: dict | None = None,k: int = 5):
        
        try:
            
            if not image_query:
                raise ValueError("Image query is missing")
            
            img_embeddings = embedding_handler.get_image_embeddings(image_query)
            
            result = self.vector_db._collection.query(
                [img_embeddings.tolist()],
                n_results=k,
                where=where,
                include=["documents","metadatas", "distances"]
                
            )
            
            ids = result.get("ids", [[]])[0]
            docs = result.get("documents", [[]])[0]
            metas = result.get("metadatas",[[]])[0]
            dists = result.get("distances",[[]])[0]
            
            results = []
            
            for id, doc, meta, dist in zip(ids, docs, metas, dists):
                results.append({
                    "doc_id": id,
                    "content": doc,
                    "metadata": meta,
                    "distance": dist
                })
            
            return results
            
        except ValueError:
            logger.exception("Value error in image query search")
            raise
        
        except Exception:
            logger.exception("Error in image query search")
            raise