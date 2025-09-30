
from pydantic import BaseModel
from datetime import datetime

class image(BaseModel):
    item_id:int
    url: str
    date_uploaaded: datetime
    
