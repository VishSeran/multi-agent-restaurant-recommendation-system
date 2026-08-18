from pydantic import BaseModel, Field

class ImageCaptionSchema(BaseModel):
    
    image_description: str = Field(
        description="Description of the image's caption"
    )