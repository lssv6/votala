from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List

class User(BaseModel):
    email: str
    hashed_password: str
    created: datetime

class Poll(BaseModel):
    id: UUID
    creator: str
    created: datetime
    valid_until: datetime
    query: str
    alternatives: List[str]
    min_number_of_choices: int
    max_number_of_choices: int

class PollPermission(BaseModel):
    poll_id: UUID
    allowed_user: str

# Created when we want to create a new user.
class NewUserRequest(BaseModel):
    email: str
    password: str
