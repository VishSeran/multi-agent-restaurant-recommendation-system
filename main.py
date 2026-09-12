

from configurations.configs import FOOD_IMAGES_URL, FOOD_RECIPE_URL, USER_REVIEWS_URL
from configurations.logger import get_logger
from data_extractor.extractor import DataExtractor


logger = get_logger("main")

async def main():
    
    
    try:
        
        data_extractor = DataExtractor()
    
        #load datasets
        data_extractor.load_dataset(url=FOOD_RECIPE_URL,
                                    file_name= "Recipes.json",
                                    directory="food_recipes")
        
        data_extractor.load_dataset(
            url=USER_REVIEWS_URL,
            file_name="Synthetic-User-Reviews.json",
            directory="user_reviews"
        )
        
        data_extractor.load_dataset(
            url=FOOD_IMAGES_URL,
            file_name="synthetic-recipe-images.zip",
            directory="synthetic_recipe_images"
        )
        
    except Exception:
        logger.exception("Error in main")
        raise