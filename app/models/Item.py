from pydantic import BaseModel
from Image import image


class item(BaseModel):
    user_id: int #user id of the person found (reg_no)
    desc: str #colour and place 
    img: image  #image for the item
    type: str #type like bottle, pen etc
    item_id: int #each reg item has random id