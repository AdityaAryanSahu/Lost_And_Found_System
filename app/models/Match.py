from pydantic import BaseModel

class MatchResponse(BaseModel):
    item_id: int
    mssg:str