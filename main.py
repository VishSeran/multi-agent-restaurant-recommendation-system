

from configurations.configs import FOOD_IMAGES_URL, FOOD_RECIPE_URL, USER_REVIEWS_URL, Base_dir
from configurations.logger import get_logger
from data_extractor.extractor import DataExtractor
from vectore_store.images_db import ImageVectorDB
from vectore_store.restaurants_db import RestaurantVectorDB


logger = get_logger("main")

async def main():
    
    
    try:
        
        data_extractor = DataExtractor()
    
        #load datasets
        await data_extractor.load_dataset(url=FOOD_RECIPE_URL,
                                    file_name= "Recipes.json",
                                    directory="food_recipes")
        
        await data_extractor.load_dataset(
            url=USER_REVIEWS_URL,
            file_name="Synthetic-User-Reviews.json",
            directory="user_reviews"
        )
        
        await data_extractor.load_dataset(
            url=FOOD_IMAGES_URL,
            file_name="synthetic-recipe-images.zip",
            directory="synthetic_recipe_images"
        )
        
        #format restaurants data
        restaurants_data = await data_extractor.get_restaurants_data()
        
        #format recipe data
        recipe_data = await data_extractor.combine_food_recipe_data_with_image_description()
        
        #formate user reviews
        user_reviews_data = await data_extractor.summarize_user_reviews()
        
        
        #get restaurant vector db
        restaurant_vector_db_obj = RestaurantVectorDB(restaurants_data)
        restaurant_vector_db = restaurant_vector_db_obj.vector_store
        
        image_vector_db_obj = ImageVectorDB(
            Base_dir/"dataset"/"synthetic_recipe_images"/"synthetic-recipe-images",
            recipe_data
        )
        
        image_vector_db = image_vector_db_obj.vector_db
        
    except Exception:
        logger.exception("Error in main")
        raise