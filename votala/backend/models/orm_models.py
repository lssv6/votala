from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import ARRAY, TIMESTAMP
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    Represents this table:
    CREATE TABLE USERS IF NOT EXISTS(
        ID UUID DEFAULT GEN_RANDOM_UUID() UNIQUE,
        EMAIL VARCHAR(254) PRIMARY KEY,
        NICKNAME VARCHAR(32) UNIQUE,
        HASHED_PASSWORD TEXT NOT NULL,
        CREATED TIMESTAMP DEFAULT NOW() NOT NULL
    );
    """

    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(
        SQLUUID(), insert_default=func.gen_random_uuid(), default=None, primary_key=True
    )
    email: Mapped[str] = mapped_column(String(254), unique=True)
    nickname: Mapped[str] = mapped_column(String(32), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    created: Mapped[datetime] = mapped_column(
        insert_default=func.now(), default=None, nullable=False
    )


class Group(Base):
    """
    Represents this table:

    CREATE TABLE GROUP IF NOT EXISTS(
        ID UUID NOT NULLL DEFAULT GEN_RANDOM_UUID(),
        NAME VARCHAR(64) NOT NULL,
        CREATOR VARCHAR(254) REFERENCES USER(EMAIL),
        CREATED TIMESTAMP NOT NULL DEFAULT
    )
    """

    __tablename__ = "groups"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(), insert_default=func.gen_random_uuid(), default=None, primary_key=True
    )
    name: Mapped[str] = mapped_column(String(64))
    creator: Mapped[str] = mapped_column(ForeignKey("users.id"))
    created: Mapped[datetime] = mapped_column(
        insert_default=func.now(), default=None, nullable=False
    )


class GroupMembership(Base):
    """
    Represents this table:

    CREATE TABLE GROUP_PARTICIPANTS IF NOT EXISTS(
        GROUP_ID UUID REFERENCES GROUP(ID),
        USER_EMAIL VARCHAR(254) REFERENCES USER(EMAIL),
        ADDED TIMESTAMP NOT NULL DEFAULT NOW(),

        CONSTRAINT UNIQUE(GROUP_ID, USER_EMAIL) -- hashes the foreign keys and makes the combination of groups and user unique.
    )
    """

    __tablename__ = "group_memberships"

    #    __table_args__ = (
    #        UniqueConstraint("group_id", "user_email"),
    #    )
    #
    group_id: Mapped[UUID] = mapped_column(ForeignKey("groups.id"), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), primary_key=True)
    admin: Mapped[bool] = mapped_column(Boolean(), default=False)
    added: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
        default=None,
        nullable=False,
    )


class Poll(Base):
    """
    Represents this table:
    CREATE TABLE POOLS IF NOT EXISTS(
        ID UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
        CREATOR VARCHAR(254) REFERENCES USERS(EMAIL),
        GROUP UUID,
        CREATED TIMESTAMP DEFAULT NOW() NOT NULL,
        VALID_UNTIL TIMESTAMP,
        TYPE TEXT NOT NULL,

        -- IF TYPE IS "CHECK" OR "RADIO"
        QUERY TEXT NOT NULL,
        ALTERNATIVES TEXT[] NOT NULL,
        MIN_NUMBER_OF_CHOICES INT,
        MAX_NUMBER_OF_CHOICES INT,

        -- IF TYPE IS "TEXTFIELD" OR "TEXTAREA" THEN THE ALTERNATIVES , MIN AND MAX ARE NULL.
    );
    """

    __tablename__ = "polls"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(), insert_default=func.gen_random_uuid(), default=None, primary_key=True
    )
    creator: Mapped[str] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[UUID] = mapped_column(ForeignKey("groups.id"))
    created: Mapped[datetime] = mapped_column(insert_default=func.now(), default=None)
    valid_until: Mapped[datetime] = mapped_column(TIMESTAMP(), nullable=True)
    query: Mapped[str] = mapped_column(Text(), nullable=False)
    alternatives: Mapped[List[str]] = mapped_column(ARRAY(Text()), nullable=False)
    min_number_of_choices: Mapped[int] = mapped_column(Integer())
    max_number_of_choices: Mapped[int] = mapped_column(Integer())


class ChoiceAwnser(Base):
    """
    Represents this table:
    CREATE TABLE AWNSER IF NOT EXISTS(
        POLL_ID UUID REFERENCES POLLS(ID),
        USER_ID UUID REFERENCES USERS(ID),
        CHOICED BOOLEAN[] NOT NULL,
        CONSTRAINT UNIQUE(POLL_ID, USER_ID)
    )
    """

    __tablename__ = "choice_awnsers"

    poll_id: Mapped[UUID] = mapped_column(ForeignKey("polls.id"), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    choiced: Mapped[List[bool]] = mapped_column(ARRAY(Boolean()), nullable=False)


class GuestChoiceAwnser(Base):
    """
    Awnsers for non-logged users.
    Represents this table:
    CREATE TABLE GUEST_CHOICE_AWNSER IF NOT EXISTS(
        POLL_ID REFERENCES POLLS(ID),
        CHOICED BOOLEAN[] NOT NULL
    )
    """

    __tablename__ = "guest_choice_awnsers"
    poll_id: Mapped[UUID] = mapped_column(ForeignKey("polls.id"), primary_key=True)
    choiced: Mapped[List[bool]] = mapped_column(ARRAY(Boolean()), nullable=False)


class TextAwnser(Base):
    """
    Represents this table:
    CREATE TABLE TEXT_AWNSER IF NOT EXISTS(
        POLL_ID UUID REFERENCES POLLS(ID),
        USER_ID UUID REFERENCES USERS(ID),
        TEXT TEXT NOT NULL,
        CONSTRAINT UNIQUE(POLL_ID, USER_ID)
    )
    """

    __tablename__ = "text_awnsers"
    #    __table_args__ = (
    #        UniqueConstraint("poll_id", "user_id"),
    #    )
    #
    poll_id: Mapped[UUID] = mapped_column(ForeignKey("polls.id"), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    text: Mapped[str] = mapped_column(Text(), nullable=False)


class NewUserRequest(Base):
    """Represents a new user request table"""

    __tablename__ = "new_user_requests"
    user_email: Mapped[str] = mapped_column(String(254), primary_key=True)
    requested: Mapped[datetime] = mapped_column(
        insert_default=func.now(), default=None, nullable=False
    )


# class GuestTextAwnser(Base):
#    """
#    Represents this table:
#    CREATE TABLE GUEST_TEXT_AWNSER IF NOT EXISTS(
#        POLL_ID UUID REFERENCES POLLS(ID),
#        TEXT TEXT NOT NULL,
#    )
#    """
#    __tablename__ = "guest_text_awnser"
#
#
#    poll_id: Mapped[UUID] = mapped_column(ForeignKey("polls.id"))
#    text: Mapped[str] = mapped_column(Text(), nullable=False)
#
