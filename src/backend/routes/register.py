from fastapi import APIRouter, Body, Depends, status
from models.models import *
from dependencies.message_broker import get_mb
from aiormq import Connection
register = APIRouter()

@register.post("/users")
async def create_newuser_request(
    new_user: NewUserRequest,
    mb:Connection = Depends(get_mb)
):
    channel  = await mb.channel()
    binary_data = bytes(new_user.json(), "UTF-8")
    await channel.basic_publish(binary_data,routing_key="new_user_request")
    return status.HTTP_201_CREATED

