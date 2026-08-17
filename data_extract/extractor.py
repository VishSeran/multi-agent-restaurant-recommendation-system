
from typing import Optional
import httpx
from pathlib import Path

from configurations.logger import get_logger


logger = get_logger('extractor')


async def load_dataset(url:str, file_path:str):
    
    try:
        
        if not url and not file_path:
            raise ValueError("Error in data loading, At leaset URL or File Path must be provided!!!")
        
        path = Path(file_path).resolve()
        
        if url and not path.exists():
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                
                logger.info("File is received")
                
                with open(path, "wb") as file:
                    file.write(response.content)
                    
                logger.info("File is created")
                
        if path.exists():
            with open(path, "r", encoding="utf-8") as file:
                    data = file.read()
                    
                    if not data:
                        raise ValueError(f"Error in data loading, cannot load the file: {file_path}")
                    
            logger.info("Data loading is completed")
            return data
                
    except ValueError:
        logger.exception("Value error in load_dataset")
        raise
    
    except Exception:
        logger.exception("Error in load_dataset")
        raise
    
def split_restaurant_data_into_list(data:str):
    
    try:
        
        if not data:
            raise ValueError("Restaurant data is missing")
        
        formatted_data = data.split("\n\n")
        formatted_data = formatted_data[1:]
        
        logger.info("Restaurant data is formatted")        
        return formatted_data
        
        
    except ValueError:
        logger.exception("Value error in split_restaurant_data_into_list")
        raise
    
    except Exception:
        logger.exception("Error in split_restaurant_data_into_list")
        raise
    
  
