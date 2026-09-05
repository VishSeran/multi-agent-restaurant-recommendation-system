from pathlib import Path
from fastmcp import Context

from fastmcp import FastMCP
from agent_workflow.workflow import MultiAgentWorkflow
from configurations.configs import CULINARY_MAP_DIR, RECIPE_DIR, RESTAURANT_DIR, USER_REVIEW_DIR
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
            self.workflow = MultiAgentWorkflow()
            self.register_tools()
            
        except Exception:
            logger.exception("Error in mcp server init")
            raise
        
    
    def get_mcp_server(self):
        return self.mcp
    
    def register_tools(self):
        
        @self.mcp.tool()
        async def read_restaurant_data(file_name:str | None, ctx:Context) ->str:
            
            """
            Read a JSON file from the restaurant dataset directory.

            Access is restricted to files located inside:
            dataset/restaurants/
            """
            
            try:
                if not file_name:
                    file_name = "structured_restaurant_data.json"
                
                requested_file = (RESTAURANT_DIR / file_name).resolve()
                
                if RESTAURANT_DIR not in requested_file.parent:
                    raise ValueError("Access outside the restaurant directory is forbidden")
                
                if requested_file.suffix.lower() != ".json":
                    raise ValueError("Only json file are allowed to read")
                
                if not requested_file.is_file():
                    raise ValueError(f"{file_name} is not found")
                
                content = requested_file.read_text(encoding="utf-8")
                await ctx.info(f"{file_name} content is fetched")
                
                return content
            
            except ValueError as e:
                await ctx.error(f"Value error in read restaurant data: {e}")
                logger.exception("Value error in read restaurant data")
                raise   
            
            except OSError as e:
                await ctx.error("Unable to read the requested file")
                logger.error("Filesystem error while reading %s: %s", file_name, e)
                raise
            
            except Exception:
                
                await ctx.error("An unexpected server error occurred")
                logger.exception(
                    "Unexpected error in read_restaurant_data for file %s",
                    file_name
                )
                raise
            

        @self.mcp.tool()
        async def read_review_data(file_name: str | None, ctx: Context):
            
            """
                Read a JSON file from the user reviews dataset directory.
            
                Access is restricted to files located inside:
                dataset/restaurants/
            """
            
            try:
                
                if not file_name:
                    file_name = "augmented_user_review.json"
                    
                requested_file = (USER_REVIEW_DIR / file_name).resolve()
                
                if USER_REVIEW_DIR not in requested_file.parent:
                    raise ValueError("Access outside the user review directory is forbidden")
                
                if requested_file.suffix.lower() != ".json":
                    raise ValueError("Only json file are allowed to read")
                
                if not requested_file.is_file():
                    raise ValueError(f"{file_name} is not found")
                
                content = requested_file.read_text(encoding="utf-8")
                await ctx.info("review data is fetched successfully")
                
                return content
                
            except ValueError as e:
                await ctx.error(f"An unexpected server error occurred: {e}")
                logger.exception(
                    "Unexpected error in read_review_data for file %s",
                    file_name
                )
                raise
            
            except Exception:
                    
                await ctx.error("An unexpected server error occurred")
                logger.exception(
                    "Unexpected error in read_review_data for file %s",
                    file_name
                )
                raise

        @self.mcp.tool()
        async def read_recipe_data(file_name:str | None, ctx:Context):
            
            try:
                
                if not file_name:
                    file_name = "augmented_food_recipe.json"
                
                requested_file = (RECIPE_DIR/file_name).resolve()
                
                if RECIPE_DIR not in requested_file.parent:
                    raise ValueError("Access outside the recipe directory is forbidden")
                
                if requested_file.suffix.lower() != ".json":
                    raise ValueError("Only json file are allowed to read")
                
                if not requested_file.is_file():
                    raise ValueError(f"{file_name} is not a file; file not found")
                
                content = requested_file.read_text(encoding="utf-8")
                await ctx.info("recipe data is fetched successfully")
                
                return content

            except ValueError as e:
                await ctx.error(f"Unexpected value error in server: {e}")
                logger.exception(
                    "Unexpected error in read recipe data for file %s",
                    file_name
                )
                raise
            
            except Exception:
                await ctx.error("Unexpected server error")
                logger.exception("Unexpected server error in %s", file_name)
                raise
            
            
        @self.mcp.resource()
        async def get_clinary_map(ctx:Context) -> str:
            
            """The full raw California Culinary Map.
            Contains detailed descriptions of 100+ restaurants across California
            including their vibes, cuisines, ratings, and price ranges."""
            
            try:
                
                return CULINARY_MAP_DIR.read_text(encoding="utf-8")
                
                
            except Exception:
                await ctx.error("Unexpected Error in get culinary map")
                logger.exception("Unexpected Error in get culinary map")
                raise

mcpserver = MCPServer()

    