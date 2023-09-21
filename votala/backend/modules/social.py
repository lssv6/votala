"""Module for database/crud operations with accouting and social """
import re
from typing import Optional
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import modules.authentication
from models import orm_models, schemas
from modules.datum import to_schemas
from modules.logs import logger as log

# Normally, this operations are made using a query that returns
# a iterable of ORM-Like data. Then I convert into an "schema" pydantic
# object. So we can use in the API.


def remove_member(session: Session, group_id: UUID, member_id: UUID):
    user = get_user_by_id(session, member_id)
    if user is not None:
        session.execute(
            delete(orm_models.GroupMembership).filter_by(
                user_id=member_id, group_id=group_id
            )
        )
        return True
    return False


def is_email(string):
    """Returns True if string is a valid email."""
    EMAIL_VALIDATION_REGEX = (
        "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?"
        ':[\x01-\x08\x0b\x0c\x0e-\x1f!#-[]-\x7f]|\\[\x01-\t\x0b\x0c\x0e-\x7f])*")@'
        "(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
        "|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0"
        "-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f!-Z"
        "S-\x7f]|\\[\x01-\t\x0b\x0c\x0e-\x7f])+)\\])"
    )
    return re.compile(EMAIL_VALIDATION_REGEX).fullmatch(string)


def change_privilege(session: Session, group_id: UUID, member_id: UUID, power: bool):
    member = get_user_by_id(session, member_id)
    if member is None:
        return False
    session.execute(
        update(orm_models.GroupMembership)
        .filter_by(group_id=group_id, member_id=member_id)
        .values(admin=power)
    )


def is_admin(session: Session, user_id: UUID, group_id: UUID) -> bool:
    data = session.execute(
        select(orm_models.GroupMembership).filter_by(group_id=group_id, user_id=user_id)
    ).scalar()
    data = schemas.GroupMembership.from_orm(data)
    return data.admin


def get_group(session: Session, group_id: str) -> schemas.Group | None:
    data = session.get(orm_models.Group, group_id)
    if data is not None:
        return schemas.Group.from_orm(data)
    return None


def add_member(session: Session, group_id: UUID, requester: UUID, user_to_add: UUID):
    is_adm = is_admin(session, requester, group_id)
    if is_adm or requester == user_to_add:
        session.add(orm_models.GroupMembership(group_id=group_id, user_id=user_to_add))
        return True
    return False


def get_user_by_email(session: Session, email: str) -> schemas.User | None:
    user = session.execute(
        select(orm_models.User).filter_by(email=email)
    ).scalar_one_or_none()
    if user is None:
        return None
    return schemas.User.from_orm(user)


def get_user_by_id(session: Session, uuid: UUID) -> schemas.User | None:
    data = session.execute(
        select(orm_models.User).where(orm_models.User.id == uuid)
    ).scalar_one_or_none()
    if data is None:
        return None
    return schemas.User.from_orm(data)


def get_all_user_info(
    session: Session, query: str | None = None
) -> list[schemas.UserPreview]:
    if query is None:
        data = session.execute(select(orm_models.User)).scalars()
        return to_schemas(schemas.UserPreview, data)

    # Return all users but filtered with query.
    data = session.execute(
        select(orm_models.User).where(
            func.substring(orm_models.User.nickname, query).is_not(None)
        )
    ).scalars()
    return to_schemas(schemas.UserPreview, data)


def create_user(session: Session, user_create: schemas.UserCreate):
    data_to_insert = {
        **user_create.dict(),
        "nickname": user_create.email,
        "hashed_password": modules.authentication.get_password_hash(
            user_create.password
        ),
    }
    session.execute(insert(orm_models.User), [data_to_insert])
    session.commit()


def is_member(session: Session, user_id: UUID, group_id: UUID) -> bool:
    """Returns true if a user with a {user_email} belongs to a group with {group_id}"""
    data = session.execute(
        select(orm_models.GroupMembership).filter_by(group_id=group_id, user_id=user_id)
    ).scalar_one_or_none()
    # Returns true if the user is member of the given group
    return data is not None


def get_groups_by_user_id(session: Session, user_id: UUID) -> list[schemas.Group]:
    """Returns the groups which a User is member."""

    datum = session.execute(
        select(orm_models.Group)
        .join(
            orm_models.GroupMembership,
            orm_models.Group.id == orm_models.GroupMembership.group_id,
        )
        .where(orm_models.GroupMembership.user_id == user_id)
    ).scalars()
    return to_schemas(schemas.Group, datum)


def get_members_by_group_id(
    session: Session, group_id: UUID
) -> list[schemas.UserPreview]:
    """Returns all the members of a given group_id."""
    datum = session.execute(
        select(orm_models.User)
        .join(
            orm_models.GroupMembership,
            orm_models.User.id == orm_models.GroupMembership.user_id,
        )
        .where(orm_models.GroupMembership.group_id == group_id)
    ).scalars()
    return to_schemas(schemas.UserPreview, datum)


def add_member_to_a_group(
    session: Session, member_id: str, group_id: str, admin: bool = False
):
    session.execute(
        insert(orm_models.GroupMembership).values(
            group_id=group_id, user_id=member_id, admin=admin
        )
    )


def create_group(
    session: Session,
    creator: schemas.User,
    group: schemas.GroupCreate,
) -> None:
    """
    Creates a group with some initial properties
    """
    initial_members = group.initial_members

    # It's the obligatory minimal data to create a new group.
    data_to_insert = {"creator": creator.id, **group.dict()}

    added_group = session.execute(  # returns the recently added group
        insert(orm_models.Group).returning(orm_models.Group),
        [data_to_insert],
    ).scalar_one()
    # add all initial members to the database as members of the group.
    for member_id in initial_members:
        add_member_to_a_group(session, member_id, str(added_group.id))
    session.commit()
