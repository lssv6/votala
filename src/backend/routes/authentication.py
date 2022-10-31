from sqlalchemy import Engine
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from modules.authentication.authentication import get_current_user, get_user, authenticate_user, create_access_token
from models.models import User
from dependencies.database import get_engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

authentication = APIRouter()


@authentication.post("/token")
async def get_token(
	form: OAuth2PasswordRequestForm = Depends(),
	engine: Engine = Depends(get_engine),
):
	user = authenticate_user(engine, form.username, form.password)
	if not user:
		raise HTTPException(status_code=400, detail="Incorrect username or password.",headers={"WWW-Authenticate":"Bearer"})
	access_token  = create_access_token(data={"sub": user.email})
	return {"access_token":access_token, "token_type":"bearer"}


@authentication.get("/users/me")
async def get_yourself(user = Depends(get_current_user)):
	return User(**user)
