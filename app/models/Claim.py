from pydantic import BaseModel


class claim(BaseModel):
    item_id:int
    user_id:int