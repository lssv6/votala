from fastapi import Request
from sqlalchemy import Engine, create_engine

from models.orm_models import *
from modules.logs import logger as log

database_connection_properties = {
    "host": "database",
    "port": 5432,
    "user": "votala",
    "password": "votala",
    "database": "postgres",
}


def get_engine(request: Request):
    orm = getattr(request.app.state, "engine", None)
    if orm is None:
        log.warning("THE ENGINE IS NULL!!!")
    return orm


def get_votala_db_engine():
    engine: None | Engine = getattr(get_votala_db_engine, "engine", None)
    if engine is None:
        log.info("Now creating the orm engine.")
        connection_template = (
            "postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
        )
        engine = create_engine(
            connection_template.format(**database_connection_properties),
        )
        log.info("Created the orm engine.")
        setattr(get_votala_db_engine, "engine", engine)
    return engine
