from passlib.context import CryptContext
from schemas import ScheduleCreate
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession 
from models import BaseClassRoom
from fastapi import status, HTTPException
from sqlalchemy import select, and_, or_

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def check_time_conflicts(db: AsyncSession, 
                               model: Type[BaseClassRoom], 
                               new_event: ScheduleCreate):
    if new_event.start_time > new_event.end_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неправильное время")
    
    conflict = await db.execute(
        select(model).where(
            model.date == new_event.date,
            model.start_time < new_event.end_time,
            model.end_time > new_event.start_time
        )
    )
    if conflict.scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Время уже было занято ")
    
    return True