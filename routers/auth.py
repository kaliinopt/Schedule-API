import models, schemas, utils, oath2
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db

router = APIRouter(tags=['Authentication'])

@router.post('/login')
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(models.User).where(models.User.username == user_credentials.username))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')

    access_token = oath2.create_access_token(data = {"user_id": user.id})


    return {"access_token": access_token, 
            "token_type": "bearer"}