from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import orm_models, schemas
from modules.datum import to_schemas
from modules.social import is_member


def get_group_polls(session: Session, group_id: UUID) -> list[schemas.Poll]:
    """Returns a ResultSet of polls"""
    data = session.execute(
        select(orm_models.Poll).where(orm_models.Poll.group_id == group_id)
    ).scalars()
    return to_schemas(schemas.Poll, data)


def create_global_poll(
    session: Session,
    *,
    creator: schemas.User,
    poll: schemas.Poll,
):
    pass


def create_poll(
    session: Session,
    *,
    creator: schemas.User,
    group_id: UUID,
    poll_create: schemas.PollCreate,
):
    obj = orm_models.Poll(
        creator=creator.id,
        group_id=group_id,
        **poll_create.dict(),
    )
    # obj = orm_models.Poll(
    #     creator=creator,
    #     group_id=group_id,
    #     valid_until=valid_until,
    #     _type=_type,
    #     query=query,
    #     alternatives=alternatives,
    #     min_number_of_choices=min_number_of_choices,
    #     max_number_of_choices=max_number_of_choices,
    # )
    session.add(obj)  # Hopefuly works
