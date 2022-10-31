from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from passlib.context import CryptContext
from jose import JWTError, jwt

from models.orm_models import UserORM
from dependencies.database import get_engine


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "8cb7565816ecb4b6c3d0eb20969822d69b6718b6d7d0e23cf2bffda3055ef66e"
ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(engine : Engine, email:str,):
	with Session(engine) as session:
		user = session.get(UserORM, email)
	return user

def authenticate_user(engine, email, password):
	user = get_user(engine, email)
	if not user:
		return False
	if not verify_password(user.password, password):
		return False
	return user

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
	to_encode = data.copy()
	expire = datetime.utcnow() + expires_delta
	to_encode.update({'exp':expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

def get_current_user(
	token: str = Depends(oauth2_scheme),
	engine:Engine = Depends(get_engine),
):
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validade credentials.",
		headers={"WWW-Authenticate": "Bearer"},
	)
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username: str = payload.get("sub")
		if username is None:
			raise credentials_exception
	except JWTError:
		raise credentials_exception
	user = get_user(engine, username)
	if user is None:
		raise credentials_exception
	return user
