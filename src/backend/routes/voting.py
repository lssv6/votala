from fastapi import APIRouter, Depends, status
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from aiormq import Connection

from dependencies.database import get_engine
from dependencies.message_broker import get_mb

from models.orm_models import PollORM, UserORM
from models.models import *

from modules.log.logs import logger as log

voting = APIRouter()

@voting.post("/poll")
async def create_new_poll(poll_data : Poll, engine:Engine= Depends(get_engine)):
    log.info("asdasd")
    print(engine)
    with Session(engine) as session:
        session.add(PollORM(**poll_data.dict()))
        session.commit()


# @voting.put("/users")
# async def create_new_user(user_data: User, engine: Engine = Depends(get_orm)):
#     with Session(engine) as session:
#         session.add(UserORM(**user_data.dict()))
#         session.commit()
