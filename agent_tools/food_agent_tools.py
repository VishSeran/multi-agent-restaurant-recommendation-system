from langchain_core.tools import tool



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


@tool
def nutrition_analze(food_name:str) -> str:
    """Analyze nutritional characteristics such as
    calories, protein, carbohydrates, fat, and general nutrition.

    Args:
        food_name (str): name of the dish

    Returns:
        str: analyze description
    """
    
    return f"Nutrition analysis for {food_name}"