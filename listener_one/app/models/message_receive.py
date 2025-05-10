from pydantic import BaseModel
from typing import Literal, Optional

class Message_receive(BaseModel):
    user_id: str
    post_id: str
    post_type: Literal["lostitem", "founditem"]
    image_data: Optional[str] # This is the base64 image string
    description: str
    item_category: str