from . import models, utils, oath2
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import get_db
import logging
from fastapi import Request

logger = logging.getLogger("app")

router = APIRouter(tags=['Authentication'])

@router.post('/login')
async def login(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(models.User).where(models.User.username == user_credentials.username))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    
    if not utils.verify(user_credentials.password, user.password):
        logger.info(f"Неудачная попытка входа {user_credentials.username} FROM {request.client.host}",)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    logger.info(
       f"Successful login as {user_credentials.username} FROM {request.client.host}",)

    access_token = oath2.create_access_token(data = {"username": user.username})
    return {"access_token": access_token, 
            "token_type": "bearer"}