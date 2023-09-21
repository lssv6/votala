from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose.jwt import JWTError
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from dependencies.database import get_engine
from models.schemas import User
from modules.authentication import decode_token
from modules.social import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    engine: Engine = Depends(get_engine),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validade credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:  # to validade credentials
        payload = decode_token(token)
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    with Session(engine) as session:
        user = get_user_by_email(session, username)

    if user is None:
        raise credentials_exception

    return User.from_orm(user)

