from pydantic import BaseModel, Field,ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any

class ImageModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[str] = Field(None, alias="_id")
    item_id: str                               
    url: str                                   
    date_uploaded: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)
    
class Image(BaseModel):
    item_id: str  # item id for the image
    url: str
    date_uploaded: datetime
    
    def to_model(self) -> ImageModel:
        return ImageModel(
            item_id=self.item_id,
            url=self.url,  
            date_uploaded=self.date_uploaded
        )

    @classmethod
    def from_model(cls, image_model: ImageModel) -> 'Image':
        return cls(
            item_id=image_model.item_id,
            url=image_model.url,  # Use url as path
            date_uploaded=image_model.date_uploaded
        )