from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.database import models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.database import get_db
from . import load_config

config = load_config()


# Схема для аутентификации OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Функция для создания JWT токена
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)

    return encoded_jwt


# Функция для проверки токена и получения пользователя
async def verify_access_token(token: str, credentials_exception, db: AsyncSession):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])

        username: str = payload.get("username")

        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(
        select(models.User).where(models.User.username == username)
    )
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user


# Dependency для получения текущего пользователя
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не смог обработать данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return await verify_access_token(token, credentials_exception, db)


# Функция для проверки роли пользователя
def require_role(role: str):
    async def role_checker(current_user: models.User = Depends(get_current_user)):
        if current_user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Отказано в доступе"
            )
        return current_user

    return role_checker
