
from configurations.logger import get_logger


logger = get_logger("mcp-client")

class MCPClient:
    
    def __init__(self):
        
        try:
            
            
        except Exception:
            logger.exception("Error in mcp client init")
            raise