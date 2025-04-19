from passlib.context import CryptContext
from .schemas import ScheduleCreate
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession 
from .models import BaseClassRoom
from fastapi import status, HTTPException
from sqlalchemy import select, and_, or_
from typing import Optional
from datetime import date, timedelta

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

# Input should be a valid date in format YYYY-MM-DD
def get_next_occurrence(
    event_date: date,
    repeat_frequency: Optional[str],
    repeat_until: Optional[date],
    week_start: date,
    week_end: date
) -> Optional[date]:
    """Вычисляет следующую дату события в пределах запрашиваемой недели"""
    if not repeat_frequency:
        return None
    
    current_date = event_date
    while current_date <= week_end:
        if current_date >= week_start:
            if not repeat_until or current_date <= repeat_until:
                return current_date
        
        # Вычисляем следующую дату в зависимости от частоты
        if repeat_frequency == "daily":
            current_date += timedelta(days=1)
        elif repeat_frequency == "weekly":
            current_date += timedelta(weeks=1)
        elif repeat_frequency == "secondweek":
            current_date += timedelta(weeks=2)
        elif repeat_frequency == "monthly":
            year = current_date.year + (current_date.month == 12)
            month = current_date.month + 1 if current_date.month < 12 else 1
            try:
                current_date = current_date.replace(year=year, month=month)
            except ValueError:
                current_date = current_date.replace(year=year, month=month, day=28)
        else:
            break
    
    return None