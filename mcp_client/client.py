from contextlib import AsyncExitStack
from mcp.client.streamable_http import streamable_http_client
from mcp.client import ClientSession
from mcp import ListToolsResult

from configurations.configs import BASE_DIR
from configurations.logger import get_logger


logger = get_logger("mcp-client")

class MCPClient:
    
    def __init__(self, server_url:str, root_dir=BASE_DIR, ai_agent = None):
        
        try:
            self.agent = ai_agent
            self.root_dir = root_dir
            self.server_url = server_url
            self.session = None
            self.exit_stack = AsyncExitStack()
            self.connected = False
            
        except Exception:
            logger.exception("Error in mcp client init")
            raise
        
        
    async def connect_to_server(self):
        
        try:
            
            if self.connected:
                raise RuntimeError("Already connected to the server")
            
            if not self.session is None:
                raise RuntimeError("Client session is already running")
            
            mcp_url = f"{self.server_url}/mcp"
            
            read,write,s_id = await self.exit_stack.enter_async_context(
                streamable_http_client(mcp_url)
            ) 
            
            logger.info("Read, Write and session id is initiated")
            
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(
                    read,
                    write,
                )
            )
            self.session.initialize()
            
            self.connected = True
            logger.info('Client session in initiated')
         
            
        except Exception:
            logger.exception("Error in mcp server connection")
            
            self.session = None
            self.connected = False
            self.exit_stack = AsyncExitStack()
            
            raise
    
    async def list_tools(self):
        
        try:
            
            if self.session is None:
                raise RuntimeError("Client session not found")
            
            tools:ListToolsResult = await self.session.list_tools()
            logger.info("Session tools are listed")
            return tools
        
        except Exception:
            logger.exception("Error in list tools")
            raise
    