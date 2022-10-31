from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import ARRAY, TIMESTAMP
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

class UserORM(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(254), primary_key=True)
    hashed_password: Mapped[str] = mapped_column(Text())
    created: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp(), default=None)

class PollORM(Base):
    __tablename__ = "polls"

    id: Mapped[UUID] = mapped_column(SQLUUID(), insert_default=func.gen_random_uuid(),default=None, primary_key=True)
    creator: Mapped[str] = mapped_column(ForeignKey("users.email"), nullable=True)
    created: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp(), default=None)
    valid_until: Mapped[datetime] = mapped_column(TIMESTAMP())
    query: Mapped[str] = mapped_column(Text(), nullable=False)
    alternatives: Mapped[List[str]] = mapped_column(ARRAY(Text()), nullable=False)
    min_number_of_choices: Mapped[int] = mapped_column(Integer(), default=1)
    max_number_of_choices: Mapped[int] = mapped_column(Integer(), default=1)

class PollPermissionORM(Base):
    __tablename__ = "allowed_users"

    poll_id: Mapped[UUID] = mapped_column(ForeignKey("polls.id"), primary_key=True)
    allowed_user:Mapped[str] = mapped_column(ForeignKey("users.email"), primary_key=True)
