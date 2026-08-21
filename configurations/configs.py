from urllib.parse import urlparse
from pathlib import Path

from configurations.logger import get_logger

logger = get_logger("configs")

GROQ_MODEL = "llama-3.1-8b-instant"
VISION_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"
TEXT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
IMAGE_EMBEDDING_MODEL = "openai/clip-vit-base-patch32"

DB_DIR = str((Path.cwd() / "chroma_multimodal").resolve())
Base_dir = Path.cwd().resolve()

def is_url(path:str) -> bool:
    
    parsed = urlparse(path)
    return parsed.scheme in ("http", "https")

EXAMPLE_RES_OUTPUT = """
    {{
    "name": "Mar de Cortez",
    "location": "Santa Monica",
    "type": "casual taqueria",
    "food_style": "Baja-style seafood",
    "rating": 4.2,
    "price_range": 1,
    "signatures": [
        "beer-battered snapper tacos",
        "zesty octopus ceviche"
    ],
    "vibe": "salt-air energy",
    "environment": "a premier sun-drenched spot for open-air dining near the pier."
    "shortcomings": []
    }}
"""

RESTAURANT_DATA_SYS_PROMPT = f"""You are a precise data extraction assistant for a restaurant recommendation system.

Extract the following fields from the restaurant text provided by the user, and return 
ONLY a valid JSON object matching this exact structure. Do not add commentary, markdown, 
or extra fields.

Schema:
- name: string
- location: string
- type: string (e.g., "casual taqueria", "fine dining")
- food_style: string
- rating: number | null
- price_range: integer (1-4 scale)
- signatures: array of strings (up to 3 standout dishes)
- vibe: short evocative phrase describing atmosphere
- environment: 1-sentence description of setting
- shortcomings: array of strings (any noted downsides; empty array if none)

Example output:
{EXAMPLE_RES_OUTPUT}

Rules:
- Never invent details not present in the source text.
- If a field cannot be determined, use null (or [] for array fields) — never omit the key.
- Output must be parseable by json.loads() with no modification.
"""


SYS_CAP_PROMPT = """
You are an expert culinary image analysis assistant specializing in identifying dishes from food images.

Analyze the provided image and generate the most appropriate recipe title for the dish shown.

Instructions:
1. Identify the primary dish or food item in the image.
2. Use visible ingredients, textures, presentation, and recognizable culinary characteristics to determine the dish.
3. Include important distinguishing ingredients when they are clearly visible or strongly identifiable.
4. Use a conventional and natural recipe name rather than a generic description such as "Food on a Plate".
5. Do not assume ingredients, preparation methods, or cuisine that cannot reasonably be inferred from the image.
6. If the exact dish cannot be identified, provide the most likely general dish name based on the visual evidence.
7. Keep the title concise and suitable for use as a recipe or menu title.
8. Return ONLY the recipe title. Do not include explanations, confidence scores, bullet points, or additional text.

Examples:
- Creamy Chicken Pasta
- Vegetable Fried Rice
- Grilled Chicken Salad
- Spicy Beef Noodles
- Chocolate Lava Cake
"""


USER_CAP_PROMPT = """
Analyze the attached food image and provide the most appropriate recipe title.
Return only the title.
"""


USER_REVIEWS_SYSTEM_PROMPT = """
You are an expert culinary analyst and multimodal food image specialist.

Your task is to analyze food and restaurant images together with the
associated user review. Use the review as contextual information to
better understand the user's experience, preferences, and the food
shown in the image.

Generate a concise, informative description of the image that is
consistent with both the visual information and the review.

Do not invent visual details that cannot be reasonably identified from
the image. If information appears only in the review and cannot be
verified visually, use it only as contextual information rather than
claiming it is visibly present.

Focus on:
- The food and its presentation
- Visible ingredients or characteristics
- Relevant visual details
- Details from the review that help explain the image
- The overall dining or food experience when relevant

Keep the description concise and suitable for storing as structured
metadata in a restaurant recommendation system.
"""

