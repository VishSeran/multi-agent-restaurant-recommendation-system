from pathlib import Path
from fastmcp import Context

from mcp_server.server import mcp_server
from configurations.logger import get_logger


logger = get_logger("mcp-server-config")

BASE_DIR = Path(__file__).resolve().parent

@mcp_server.tool()
def read_restaurant_data(file_name:str, ctx:Context) ->str:
    
    try:
        if not file_name:
            raise ValueError("File name is missing")
        
        requested_file = (BASE_DIR/"dataset"/"restaurants"/file_name)
        
        if BASE_DIR not in requested_file.parent:
            raise ValueError("Access outside the restaurant directory is forbidden")
        
        if requested_file.suffix != ".json":
            raise ValueError("Only json file are allowed to read")
        
        if not requested_file.is_file():
            raise ValueError(f"{file_name} is not found")
        
        content = requested_file.read_text(encoding="utf-8")
        ctx.info(f"{file_name} content is fetched")
        
        return content
        
        
        
    except Exception:
        logger.exception("Error in read restaurant data")
        raise


