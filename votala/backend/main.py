"""
VOTALA backend file. This is the main file responsible for integrating all the
routes for serving them with uvicorn.
"""


# from dependencies.message_broker import create_votala_amqp_connection
from fastapi import FastAPI

from dependencies.database import get_votala_db_engine
from models.orm_models import Base
from modules.logs import logger as log
from routes.authentication import authentication
from routes.polling import polling
from routes.social import social_groups, social_users

app = FastAPI(
    title="VOTALA",
    description="This is the RESTful API for the VOTALA system.",
    root_path="/api",
)

app.include_router(polling)
app.include_router(authentication)
app.include_router(social_groups)
app.include_router(social_users)


@app.on_event("startup")
def startup():
    """Creates all the necessary connections with other services."""

    # Startup the sqlalchemy connection to the database
    # using the defined ORM models.
    engine = get_votala_db_engine()
    Base.metadata.create_all(bind=engine)  # Create tables if it doesn't exists
    log.info("Succesfully bound the engine to ORM")
    # Create the anonymous account for non logged polls
    setattr(app.state, "engine", engine)

    # Startup an connection to message broker.
    # message_broker = await create_votala_amqp_connection()
    # # Ensure the queue is declared
    # await (await message_broker.channel()).queue_declare("new_user_request")
    # Set it global
    # setattr(app.state, "message_broker", message_broker)


@app.on_event("shutdown")
def shutdown():
    """Just close all the connection with other services."""
    log.info("Shutting down the FastAPI Service.")
