from contextlib import AsyncExitStack
from configurations.configs import BASE_DIR
from configurations.logger import get_logger


logger = get_logger("mcp-client")

class MCPClient:
    
    def __init__(self, server_url:str, root_dir=BASE_DIR, ai_agent = None):
        
        try:
            self.agent = ai_agent
            self.root_dir = root_dir
            self.session = None
            self.exit_stack = AsyncExitStack()
            self.connected = False
            
        except Exception:
            logger.exception("Error in mcp client init")
            raise