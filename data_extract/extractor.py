
from typing import Optional
import httpx
from pathlib import Path

from configurations.logger import get_logger


logger = get_logger('extractor')


async def load_dataset(url:Optional[str], file_path:Optional[str]):
    
    try:
        
        if not url or not file_path:
            raise ValueError("Error in data loading, At leaset URL or File Path must be provided!!!")
        
        path = Path(file_path).resolve()
        
        if url and not path.exists():
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                
                logger.info("File is received")
                
                with open(path, "w") as file:
                    file.write(response.content)
                    
                logger.info("File is created")
                
        if path.exists():
            with open(path, "r") as file:
                    data = file.read()
                    
                    if not data:
                        raise ValueError(f"Error in data loading, cannot load the file: {file_path}")
                    
            logger.info("Data loading is completed")
            return data
                
            
            
        
    except ValueError:
        logger.exception("Value erro in load_dataset")
        raise
    
    except Exception:
        logger.exception("Error in load_dataset")
        raise