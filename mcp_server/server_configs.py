from pathlib import Path
from fastmcp import Context

from mcp_server.server import mcp_server
from configurations.logger import get_logger


logger = get_logger("mcp-server-config")

BASE_DIR = Path(__file__).resolve().parent
RESTAURANT_DIR = (BASE_DIR / "dataset" / "restaurants").resolve()
USER_REVIEW_DIR = (BASE_DIR / "dataset" / "user_reviews").resolve()

@mcp_server.tool()
async def read_restaurant_data(file_name:str | None, ctx:Context) ->str:
    
    """
    Read a JSON file from the restaurant dataset directory.

    Access is restricted to files located inside:
    dataset/restaurants/
    """
    
    try:
        if not file_name:
            file_name = "structured_restaurant_data.json"
        
        requested_file = (RESTAURANT_DIR / file_name).resolve()
        
        if RESTAURANT_DIR not in requested_file.parent:
            raise ValueError("Access outside the restaurant directory is forbidden")
        
        if requested_file.suffix.lower() != ".json":
            raise ValueError("Only json file are allowed to read")
        
        if not requested_file.is_file():
            raise ValueError(f"{file_name} is not found")
        
        content = requested_file.read_text(encoding="utf-8")
        await ctx.info(f"{file_name} content is fetched")
        
        return content
    
    except ValueError as e:
        await ctx.error(f"Value error in read restaurant data: {e}")
        logger.exception("Value error in read restaurant data")
        raise   
    
    except OSError as e:
        await ctx.error("Unable to read the requested file")
        logger.error("Filesystem error while reading %s: %s", file_name, e)
        raise
    
    except Exception:
        
        await ctx.error("An unexpected server error occurred")
        logger.exception(
            "Unexpected error in read_restaurant_data for file %s",
            file_name
        )
        raise
    

@mcp_server.tool()
async def read_review_data(file_name: str | None, ctx: Context):
    
    """
        Read a JSON file from the user reviews dataset directory.
    
        Access is restricted to files located inside:
        dataset/restaurants/
    """
    
    try:
        
        if not file_name:
            file_name = "augmented_user_review.json"
            
        requested_file = (USER_REVIEW_DIR / file_name).resolve()
        
        if USER_REVIEW_DIR not in requested_file.parent:
            raise ValueError("Access outside the restaurant directory is forbidden")
        
        if requested_file.suffix.lower() != ".json":
            raise ValueError("Only json file are allowed to read")
        
        if not requested_file.is_file():
            raise ValueError(f"{file_name} is not found")
        
        content = requested_file.read_text(encoding="utf-8")
        return content
        
    except ValueError as e:
        await ctx.error(f"An unexpected server error occurred: {e}")
        logger.exception(
            "Unexpected error in read_review_data for file %s",
            file_name
        )
        raise
    
    except Exception:
            
        await ctx.error("An unexpected server error occurred")
        logger.exception(
            "Unexpected error in read_review_data for file %s",
            file_name
        )
        raise


async def read_recipe_data(file_name:str | None, ctx:Context):
    
    try:
        
    except ValueError as e:
        await ctx.error(f"Unexpected value error in server: {e}")
        logger.exception(
            "Unexpected error in read recipe data for file %s",
            file_name
        )
        raise
    
    except Exception:
        await ctx.error("Unexpected server error")
        logger.exception("Unexpected server error in %s", file_name)
        raise