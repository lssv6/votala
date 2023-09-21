from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

################################################################################
### JWTToken


class JWTToken(BaseModel):
    access_token: str
    token_type: str


################################################################################
### SchemaBase is a class for being a base for ORM -> pydantic transformations.
class SchemaBase(BaseModel):
    """Base schema for ORM compatible classes."""

    class Config:
        # orm_mode = True
        from_attributes = True


################################################################################
### User


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    nickname: str
    password: str


class User(UserBase, SchemaBase):
    id: UUID
    nickname: str
    hashed_password: str
    created: datetime


class UserPreview(SchemaBase):
    id: UUID
    nickname: str
    created: datetime


################################################################################
### Poll
class PollBase(BaseModel):
    query: str
    alternatives: list[str]
    min_number_of_choices: int
    max_number_of_choices: int

    valid_until: Optional[datetime]


class PollCreate(PollBase):
    pass


class Poll(PollBase, SchemaBase):
    id: UUID
    creator: str
    created: datetime
    group_id: UUID


################################################################################
### Group
class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    initial_members: list[str] = Field(
        ..., min_items=3
    )  # Must have at least 3 members.


class Group(GroupBase, SchemaBase):
    id: UUID
    creator: UUID
    created: datetime


################################################################################
### NewUserRequest
class NewUserRequestBase(BaseModel):
    pass


class NewUserRequestCreate(NewUserRequestBase):
    email: str


class NewUserRequest(NewUserRequestBase, SchemaBase):
    created: datetime


################################################################################
### GroupMembership
class GroupMembership(SchemaBase):
    group_id: UUID
    user_id: UUID
    admin: bool
    added: datetime
