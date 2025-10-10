
from pydantic import BaseModel
from datetime import datetime

class Image(BaseModel):
    item_id:str #item id for the image
    path: str
    date_uploaded: datetime
    
