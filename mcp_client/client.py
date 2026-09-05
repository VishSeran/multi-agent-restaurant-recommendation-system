from mcp.client import St
from configurations.logger import get_logger


logger = get_logger("mcp-client")

class MCPClient:
    
    def __init__(self, server_url):
        
        try:
            self.agent = None
            self.session = None
            self.exit_stack = None
            self.connected = False
            
        except Exception:
            logger.exception("Error in mcp client init")
            raise