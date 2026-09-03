from pathlib import Path

from mcp_server.server import mcp_server
from configurations.logger import get_logger


logger = get_logger("mcp-server-config")

BASE_DIR = Path(__file__).resolve().parent

mcp_server.tool()
def read_restaurant_data(file_name:str) ->str:
    


