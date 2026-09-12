
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
        
    
    async def conversation(self, user_query:str):
        
        try:
            
            if not user_query:
                raise ValueError("User query is missing")
            
            print("Type q or quit to exit the conversation")
            
            
            if user_query.strip().lower() in (('q', 'quit')):
                print("Exiting the convesation...")
                break
            
        except ValueError as e:
            logger.error("value error in conversation")
            raise
        
        except Exception:
            logger.exception("Error in conversation")
            raise
        
        
        