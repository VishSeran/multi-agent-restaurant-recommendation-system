from langchain_core.tools import tool

from configurations.logger import get_logger


logger = get_logger("food-agent")

@tool
def food_analyze(food_name:str):
    
    """Analzye a food item, including ingredients, taste, preparation style
    , and general characteristics
    """
    
    return f"Food analysis for {food_name}"

