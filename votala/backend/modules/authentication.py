from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from models.schemas import User
from modules.logs import logger as log
from modules.social import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS512"
SECRET_KEY = "eaae9f4a59e58b0f033c928d37ba781f78f76122ac05b9b8c9225dde7e90fc0b"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class CannotAuthenticate(Exception):
    pass


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def authenticate_user(password: str, user: User) -> bool:
    if user is None:
        raise ValueError(f"Cannot authenticate a user which is {None}. {user=}")
    return verify_password(password, user.hashed_password)


def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
