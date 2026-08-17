
from typing import Optional

from configurations.logger import get_logger


logger = get_logger('extractor')


async def load_dataset(url:Optional, file_path:Optional):
    
    try:
        
        
    except ValueError:
        logger.exception("Value erro in load_dataset")
        raise
    
    except Exception:
        logger.exception("Error in load_dataset")
        raise