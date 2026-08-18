import json
from pathlib import Path

import httpx

from agents.llm_handler import LLMHandler
from configurations.configs import RESTAURANT_DATA_SYS_PROMPT, Base_dir
from configurations.logger import get_logger
from schema.restaurant import Restaurant

logger = get_logger('extractor')

class DataExtractor:
    
    def __init__(self, url: str | None, file_path:str | None, file_name: str | None):
        
        llm_handler = LLMHandler()
        self.llm = llm_handler.get_llm()
        self.restaurants_data = None          
        self.food_recipe_data = None
        self.user_reviews = None
        self.synthetic_recipes = None
        
    async def load_dataset(self, 
                           file_path:str | None,
                           file_name:str |None ,
                           url:str| None, 
                           directory:str):
        
        try:
            
            if not url and not file_path:
                raise ValueError("Error in data loading, At leaset URL or File Path must be provided!!!")
            
            if file_path:
                
                path = Path(file_path).resolve()
                if path.exists():
                    data = self.read_file(path)
                    self.restaurants_data = data
                    logger.info("Data loading is completed")
                    return
                
                elif not url:
                        raise FileNotFoundError(f"File not found and no URL provided: {path}")
                        
            if url:
                if not file_name:
                    raise ValueError(
                        "File path must be provided when downloading data"
                    )
                    
                dataset_dir = Base_dir / "dataset"/ directory
                dataset_dir.mkdir(parents=True, exist_ok=True)
                file_download_path = dataset_dir / file_name
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(url)
                    response.raise_for_status()
                    
                    logger.info("File is received")
                    
                    with open(file_download_path, "wb") as file:
                        file.write(response.content)
                        
                    logger.info("File is created")
                    
                self.restaurants_data = self.read_file(file_download_path)
                logger.info("Data loading is completed")
                return
      
        except ValueError:
            logger.exception("Value error in load_dataset")
            raise
        
        except Exception:
            logger.exception("Error in load_dataset")
            raise
        
    def  read_file(self, path):
    
        with open(path, "r", encoding="utf-8") as file:
            data = file.read()
            if not data:
                raise ValueError(f"Error in data loading, cannot load the file: {path}")
            
            return data

        
    def split_restaurant_data_into_list(self):
        
        try:
            
            if not self.restaurants_data:
                raise ValueError("Restaurant data is missing")
            
            formatted_data = self.restaurants_data.split("\n\n")
            formatted_data = formatted_data[1:]
            
            logger.info("Restaurant data is formatted")        
            return formatted_data

        except ValueError:
            logger.exception("Value error in split_restaurant_data_into_list")
            raise
        
        except Exception:
            logger.exception("Error in split_restaurant_data_into_list")
            raise
        
        
    async def get_restaurant_data(self, data):
        
        try:
            
            if not data:
                raise ValueError("restaurant data is missing")
            
            structured_llm = self.llm.with_structured_output(Restaurant)
            
            response = await structured_llm.ainvoke({
                "messages": [
                    {
                        "role": "system",
                        "content": RESTAURANT_DATA_SYS_PROMPT
                        
                    },
                    {
                        "role": "user",
                        "content": data
                    }
                ]
            })
            
            logger.info("Response has fetched")
            return response
            
        except ValueError:
            logger.exception("Value error in get_restaurant_data")
            raise
        
        except Exception:
            logger.exception("Error in get_restaurant_data")
            raise
        
        
    async def get_restaurants_data(self):
        
        try:
            formatted_data = self.split_restaurant_data_into_list()
            
            restaurants_summary = []
            total_len = len(formatted_data)
            
            filename = "structured_restaurant_data.json"
            dataset_dir = Base_dir / "dataset"
            dataset_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = dataset_dir / filename
            
            if file_path.exists():
                logger.info(
                    "Structured restaurant dataset already exists"
                )
                return self.read_file(file_path)
            
            for i,restaurant_data in enumerate(formatted_data):
                
                logger.info(f"processing restaurant {i+1}")
                response = await self.get_restaurant_data(restaurant_data)
                logger.info(f"restaurant {i+1} process is finished")
                
                restaurants_summary.append(response.model_dump())
                logger.info(f"completed: {i+1}/{total_len}")
            
            with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(restaurants_summary, file,indent=4)
                    
            logger.info(f"{filename} is  created successfully")
            return restaurants_summary
        
        except Exception:
            logger.exception("Error in get_restaurants_data")
            raise
        
        
        
    async 
  
