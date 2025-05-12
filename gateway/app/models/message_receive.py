from pydantic import BaseModel
from typing import Literal, Optional

class MessageReceive(BaseModel):
    user_id: str
    post_id: str
    post_type: Literal["lostitem", "founditem"]
    image_data: Optional[str] = None
    description: str
    item_category: str