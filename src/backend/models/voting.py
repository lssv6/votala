from uuid import UUID
from pydantic import BaseModel
from typing import Tuple
from datetime import datetime
class Vote(BaseModel):
    user_id: UUID
    poll_id: UUID
    alternatives_checked : Tuple[bool]

class Poll(BaseModel):
    user_id : UUID
    creator : UUID
    created : datetime
    valid_until : datetime
    query : str
    alternatives : Tuple[str]
    min_number_of_checks : int
    max_number_of_checks : int

