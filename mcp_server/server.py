
from fastmcp import FastMCP
from configurations.logger import get_logger


logger = get_logger("mcp-server")

class MCPServer:
    
    def __init__(self):
        
        try:
            
            self.mcp = FastMCP(
                name="RestaurantRecommendationServer",
                instructions="""
                This MCP server provides personalized restaurant recommendations.

                Use the available tools to:
                - Retrieve restaurants based on the user's query.
                - Consider cuisine, location, budget, dietary needs, and preferences.
                - Analyze the user's review history when available.
                - Find relevant restaurant details and associated images.
                - Return ranked restaurant recommendations with clear reasons.

                Do not invent restaurant information. Use only the data returned by
                the server's tools and resources. If there is insufficient information,
                clearly indicate what additional details are required.
                """,
            )
            
        except Exception:
            logger.exception("Error in mcp server init")
            raise
        
    
    def get_mcp_server(self):
        return self.mcp
    
    
mcpserver = MCPServer()
mcp_server = mcpserver.get_mcp_server()
    