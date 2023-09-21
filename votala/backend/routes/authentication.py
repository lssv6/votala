"""
This modules cares about the authentication endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from dependencies.database import get_engine
from models.custom_responses import ServerMessage
from models.schemas import JWTToken
from modules.authentication import authenticate_user, create_access_token
from modules.social import get_user_by_email

### There is the scheme for authentication.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

authentication = APIRouter(tags=["authentication"])


@authentication.post(
    "/token",
    responses={
        200: {"model": JWTToken, "description": "A successful login was completed."},
        403: {"model": ServerMessage, "description": "Cause validate credentials."}
    },
)
async def get_token(
    form: OAuth2PasswordRequestForm = Depends(),
    engine: Engine = Depends(get_engine),
):
    """Transforms a form entry into a token"""
    with Session(engine) as session:
        user = get_user_by_email(session, form.username)

    if user is None:
        response = JSONResponse(
            content=ServerMessage(message="Cannot find a user with this email.").dict(),
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
        return response
    is_password_correct = authenticate_user(form.password, user)

    if not is_password_correct:
        response = JSONResponse(
            content=ServerMessage(message="Incorrect password.").dict(),
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
        return response

    access_token = create_access_token(data={"sub": user.email})
    return JWTToken(access_token=access_token, token_type="bearer")


# @authentication.get("/users/me")
# async def get_yourself(user=Depends(get_current_user)):
#    """This endpoint simply returns the confidential credentials from the user.
#    Will be removed in production.
#    """
#    return user
#
