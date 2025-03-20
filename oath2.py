from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import schemas, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db


#Настройка JWT
SECRET_KEY = '3123c31f3384942c7ec1c434b0018faba42d0717036f35e3d192e31f40ea9551'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encooded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encooded_jwt

#сопоставление токенов
def verify_access_token(token: str, credentials_exeption):
    pass
#7:16:11