
from configurations.logger import get_logger


logger = get_logger("mcp-http-host-app")

class MCPHttpHostApp:
    
    def __init__(self):
        
        try:
            
        except Exception:
            logger.exception("Error in Http host app")
            raise