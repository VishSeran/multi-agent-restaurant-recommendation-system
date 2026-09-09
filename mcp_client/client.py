from contextlib import AsyncExitStack
from mcp.client.streamable_http import streamable_http_client
from mcp.client import ClientSession
from mcp import ListToolsResult,ListResourcesResult
from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools


from configurations.configs import BASE_DIR
from configurations.logger import get_logger
from llms.llm_handler import LLMHandler


logger = get_logger("mcp-client")

class MCPClient:
    
    def __init__(self, server_url:str, root_dir=BASE_DIR, ai_agent = None):
        
        try:
            self.agent = ai_agent
            self.client_llm_handler = LLMHandler(temperature=0.2)
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
        
        
    async def list_resources(self):
        
        try:
            if self.session is None:
                raise RuntimeError("Client session not found")
            
            resources:ListResourcesResult = await self.session.list_resources()
            logger.info("Session resources are listed")
            return resources
            
        except Exception:
            logger.exception("Error in session resources listing")
            raise
    
    async def init_agent(self):
        
        try:
            
            if not self.agent is None:
                logger.info("Agent is already running") 
                
            tools = await load_mcp_tools(self.session)
            logger.info("Tools are listed")
            
            self.agent = create_agent(
                model=self.client_llm_handler.get_llm(),
                tools=tools,
                system_prompt="""
                """
            )
            
        except Exception:
            logger.exception("Error in init agent")
            raise 