"""This module simply stores the endpoints related to voting"""
from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from dependencies.authentication import get_current_user
from dependencies.database import get_engine
from models.schemas import *
from modules.polling import *

polling = APIRouter(tags=["pooling"])


@polling.post("/polls")
def post_polls(
    poll_data: PollCreate,
    current_user: User = Depends(get_current_user),
    engine: Engine = Depends(get_engine),
):
    with Session(engine) as session:
        create_global_poll(session, **poll_data.dict(), creator=current_user)


@polling.get("/groups/{group_id}/polls")
def get_polls(
    group_id: UUID = Path(...),
    current_user: User = Depends(get_current_user),
    engine: Engine = Depends(get_engine),
):
    with Session(engine) as session:
        if is_member(session, current_user.id, group_id):
            return get_group_polls(session, group_id)
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "You can't see others group polls"},
    )


@polling.post("/groups/{group_id}/polls")
def create_new_poll(
    poll_data: PollCreate,
    group_id: UUID = Path(...),
    current_user: User = Depends(get_current_user),
    engine: Engine = Depends(get_engine),
):
    with Session(engine) as session:
        if is_member(session, current_user.id, group_id):
            create_poll(
                session, creator=current_user, group_id=group_id, poll_create=poll_data
            )
        session.commit()
