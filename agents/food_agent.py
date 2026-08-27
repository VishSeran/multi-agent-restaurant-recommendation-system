from langchain_core.tools import tool

from configurations.logger import get_logger


logger = get_logger("food-agent")

@tool
def food_analyze(food_name:str) -> str:
    
    """Analzye a food item, including ingredients, taste, preparation style
    , and general characteristics
    """
    
    return f"Food analysis for {food_name}"

@tool
def food_style_analyze (food_name:str) -> str:
    
    """Identify the cuisine and food style of a dish
    """
    
    return f"food style analysis for {food_name}"


