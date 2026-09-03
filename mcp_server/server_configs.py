from pathlib import Path
from fastmcp import Context

from mcp_server.server import mcp_server
from configurations.logger import get_logger


logger = get_logger("mcp-server-config")

BASE_DIR = Path(__file__).resolve().parent
RESTAURANT_DIR = (BASE_DIR / "dataset" / "restaurants").resolve()

@mcp_server.tool()
def read_restaurant_data(file_name:str, ctx:Context) ->str:
    
    """
    Read a JSON file from the restaurant dataset directory.

    Access is restricted to files located inside:
    dataset/restaurants/
    """
    
    try:
        if not file_name:
            raise ValueError("File name is missing")
        
        requested_file = (RESTAURANT_DIR / file_name).resolve()
        
        if RESTAURANT_DIR not in requested_file.parent:
            raise ValueError("Access outside the restaurant directory is forbidden")
        
        if requested_file.suffix.lower() != ".json":
            raise ValueError("Only json file are allowed to read")
        
        if not requested_file.is_file():
            raise ValueError(f"{file_name} is not found")
        
        content = requested_file.read_text(encoding="utf-8")
        ctx.info(f"{file_name} content is fetched")
        
        return content
    
    except ValueError as e:
        ctx.error(f"Value error in read restaurant data: {e}")
        logger.exception("Value error in read restaurant data")
        raise   
    
    except OSError as e:
        ctx.error("Unable to read the requested file")
        logger.error("Filesystem error while reading %s: %s", file_name, e)
        raise
    
    except Exception:
        ctx.error("An unexpected server error occurred")
        logger.exception(
            "Unexpected error in read_restaurant_data for file %s",
            file_name
        )
        raise


