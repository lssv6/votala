"""
VOTALA backend file. This is the main file responsible for integrating all the
routes for serving them with uvicorn.
"""

from fastapi import FastAPI
from routes.voting import voting
from routes.authentication import authentication
from routes.register import register
from models.orm_models import *
from dependencies.database import get_votala_db_engine
from dependencies.message_broker import create_votala_amqp_connection
from modules.log.logs import logger as log

app_properties = {
    "title":"VOTALA",
    "description":"""This is the RESTful API for the VOTALA system.""",
    "docs_url":"/"
}
app = FastAPI(**app_properties)

app.include_router(voting)
app.include_router(authentication)
app.include_router(register)

@app.on_event("startup")
async def startup():
    log.info("Starting the FastAPI Service")
    # Startup the sqlalchemy connection to the database
    # using the defined ORM models.
    engine = get_votala_db_engine()
    Base.metadata.create_all(engine)# Create tables if it doesn't exists
    setattr(app.state, "engine", engine)

    # Startup an connection to message broker.
    mb = await create_votala_amqp_connection()
    # Ensure the queue is declared
    await (await mb.channel()).queue_declare("new_user_request")
    # Set it global
    setattr(app.state, "message_broker", mb)

@app.on_event("shutdown")
async def shutdown():
    log.info("Shutting down the FastAPI Service.")
    engine = get_votala_db_engine()
