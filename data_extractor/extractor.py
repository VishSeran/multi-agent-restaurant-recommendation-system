import json
import ast
from pathlib import Path
from typing import Literal
import zipfile

import httpx

from llms.llm_handler import LLMHandler
from configurations.configs import RESTAURANT_DATA_SYS_PROMPT, Base_dir
from configurations.logger import get_logger
from llms.vision_llm_handler import VisionLLMHandler
from schema.restaurant import Restaurant

logger = get_logger('extractor')

class DataExtractor:
    
    def __init__(self):
        
        llm_handler = LLMHandler()
        logger.info("LLM handler connected to data extractor")
        
        self.vision_handler = VisionLLMHandler()
        logger.info("Vision handler connected to data extractor")
        
        self.llm = llm_handler.get_llm()
        self.restaurants_data = None          
        self.food_recipe_data = None
        self.user_reviews = None
        self.synthetic_recipe_images = None
        
    async def load_dataset(self, 
                           file_path:str | None,
                           file_name:str |None ,
                           url:str| None, 
                           directory:Literal["restaurants", 
                                             "food_recipes", 
                                             "user_reviews", 
                                             "synthetic_recipe_images"]):
        
        try:
            
            if not url and not file_path:
                raise ValueError("Error in data loading, At leaset URL or File Path must be provided!!!")
            
            if file_path:
                
                path = Path(file_path).resolve()
                if path.exists():
                    data = self.read_file(path)
                    
                    if path.parent.name == "restaurants":
                        self.restaurants_data = data
                    elif path.parent.name == "food_recipes":
                        self.food_recipe_data = data
                    elif path.parent.name == "user_reviews":
                        self.user_reviews = data
                    elif path.parent.name == "synthetic_recipe_images":
                        self.synthetic_recipe_images = data
                    else:
                        raise RuntimeError(f"{directory} is not a supported dataset directory")
                    
                    logger.info("Data loading is completed")
                    return
                
                elif not url:
                        raise FileNotFoundError(f"File not found and no URL provided: {path}")
                        
            if url:
                if not file_name:
                    raise ValueError(
                        "File path must be provided when downloading data"
                    )
                    
                if not directory:
                    raise ValueError(
                        "Directory must be provided when downloading data"
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
                    
                data = self.read_file(file_download_path)
                
                if directory == "restaurants":
                    self.restaurants_data = data
                elif directory == "food_recipes":
                    self.food_recipe_data = data
                elif directory == "user_reviews":
                    self.user_reviews = data
                elif directory == "synthetic_recipe_images":
                    self.synthetic_recipe_images = data
                else:
                    raise RuntimeError(f"{directory} is not a supported dataset directory")
                
                logger.info("Data loading is completed")
                return
      
        except ValueError:
            logger.exception("Value error in load_dataset")
            raise
        
        except Exception:
            logger.exception("Error in load_dataset")
            raise
        
    def  read_file(self, path:Path):
        
        if path.name.endswith(".zip"):
            
            extract_dir = path.parent / path.stem
            extract_dir.mkdir(parents=True, exist_ok=True)
            
            with zipfile.ZipFile(path, "r") as zip_file:
                zip_file.extractall(extract_dir)
                
            logger.info(f"ZIP file extracted to: {extract_dir}")
            return extract_dir
        
        
        if path.name.endswith(".rar"):
            raise NotImplementedError(
                "RAR files are not currently supported"
            )

        
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
        
        
        
    async def combine_food_recipe_data_with_image_description(self):
        
        try:
            
            food_recipes_list = json.loads(self.food_recipe_data)
            logger.info("Food recipe list is imported")
            
            for i,item in enumerate(self.synthetic_recipe_images.iterdir()):
                
                if item.is_file():
                    img_data_url = self.vision_handler.img_to_data_url(item)
                    logger.info(f"{item}'s data url has proccessed")
                    
                    img_caption = await self.vision_handler.get_vision_response(img_data_url)
                    logger.info("Image caption has fetched")
                    
                    recipe_item = food_recipes_list[i]
                    recipe_item["image_description"] = img_caption
                    
                    logger.info("Recipe is updated with image description")
                    
                logger.info("Food recipe list update is completed")
                
            filename = 'augmented_food_recipe.json'
            data_directory = Base_dir/ "dataset" / "food_recipes"
            data_directory.mkdir(parents=True, exist_ok=True)
            
            filepath = data_directory / filename
            
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(food_recipes_list, file, indent=4)
                
            logger.info(f"{filename} is saved in {filepath} successfully")
            
        except Exception:
            logger.exception("Error in combine_food_recipe_data_with_image_description")
            raise
  
  
    async def summarize_user_reviews(self):
        
        try:
            
            user_reviews_list = json.loads(self.user_reviews)
            logger.info("user reviews converted to python list")
            
            for idx, review in enumerate(user_reviews_list):
                
                title = review['title']
                text = review['text']
                
                images = ast.literal_eval(review['images'])
                
                image_data = []
                for image in images:
                    img_data_url = await self.vision_handler.img_to_data_url(image)
                    image_data.append(img_data_url)
                    
                
                
                
            
        except Exception:
            logger.exception("Error in summarize user reviews")
            raise