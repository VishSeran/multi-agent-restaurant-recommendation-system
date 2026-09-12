
from configurations.logger import get_logger
from mcp_client.client import MCPClient
from mcp_server.server import MCPServer


logger = get_logger("mcp-http-host-app")

class MCPHttpHostApp:
    
    def __init__(self, mcp_server, mcp_client):
        
        try:
            
            self.mcp_client:MCPClient = mcp_client
            self.mcp_server:MCPServer = mcp_server
            
        except Exception:
            logger.exception("Error in Http host app")
            raise
        
        
    async def connect_with_client(self):
        
        try:
            
            await self.mcp_client.connect_to_server()
            logger.info("client-server connected successfully")
            
        except Exception:
            logger.exception("Error in connect with client")
            raise
        
    
    async def get_client_response(self,query):
        
        try:
            
            
        except ValueError:
            logger.exception("Value error")
            raise
        
        except Exception:
            logger.exception("Error in get client response")
            raise