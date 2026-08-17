
from typing import Optional
import httpx
from pathlib import Path

from configurations.configs import Base_dir
from configurations.logger import get_logger


logger = get_logger('extractor')




class DataExtractor:
    
    def __init__(self, url: str | None, file_path:str | None, file_name: str | None):
        
        self.url = url
        self.file_path = file_path     
        self.file_name = file_name
        self.data = None          

    async def load_dataset(self):
        
        try:
            
            if not self.url and not self.file_path:
                raise ValueError("Error in data loading, At leaset URL or File Path must be provided!!!")
            
            if self.file_path:
                
                path = Path(self.file_path).resolve()
                if path.exists():
                    data = self.read_file(path)
                    self.data = data
                    logger.info("Data loading is completed")
                    return
                        
            if self.url:
                if not self.file_name:
                    raise ValueError(
                        "File path must be provided when downloading data"
                    )
                    
                dataset_dir = Base_dir / "dataset"
                dataset_dir.mkdir(parents=True, exist_ok=True)
                file_download_path = dataset_dir / {self.file_name}
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(self.url)
                    response.raise_for_status()
                    
                    logger.info("File is received")
                    
                    with open(file_download_path, "wb") as file:
                        file.write(response.content)
                        
                    logger.info("File is created")
                    
                self.data = self.read_file(file_download_path)
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
            
            if not self.data:
                raise ValueError("Restaurant data is missing")
            
            formatted_data = self.data.split("\n\n")
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
            
            
    
  
