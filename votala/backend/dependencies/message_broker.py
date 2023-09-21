import aiormq
from fastapi import Request

message_broker_properties = {
    "user": "guest",
    "password": "guest",
    "host": "message_broker",
}


async def create_votala_amqp_connection():
    connection_template = "amqp://{user}:{password}@{host}/"
    return await aiormq.connect(connection_template.format(**message_broker_properties))


def get_mb(request: Request):
    message_broker: aiormq.Connection | None = getattr(
        request.app.state, "message_broker"
    )
    return message_broker
