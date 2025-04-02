import models, schemas, oath2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from database import get_db
from typing import List
from datetime import date, timedelta
from typing import Optional

audience_models = {
            142: models.Class_142, 
            143: models.Class_143, 
            251: models.Class_251, 
            252: models.Class_252, 
            253: models.Class_253, 
            254: models.Class_254, 
            255: models.Class_255, 
            339: models.Class_339, 
            340: models.Class_340, 
            341: models.Class_341, 
            342: models.Class_342, 
            343: models.Class_343
        }


router = APIRouter(
    prefix="/api/schedule",
    tags=["Schedule"]
)
# Input should be a valid date in format YYYY-MM-DD
@router.get("/{audience_id}/{date_of}", response_model=List[schemas.ScheduleResponse])
async def get_schedule_for_date(
    audience_id: int, 
    date_of: date,
    db: AsyncSession = Depends(get_db)
):
    model = audience_models.get(audience_id)
    if not model:
        raise HTTPException(status_code=404, detail='Аудитория не найдена')
    
    schedule = await db.execute(
        select(model).where(model.date == date_of)
    )
    
    return schedule.scalars().all()


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

@router.get("/{audience_id}/week/{start_date}", response_model=List[schemas.ScheduleResponse])
async def get_week_schedule(
    audience_id: int,
    start_date: date,
    db: AsyncSession = Depends(get_db)
):
    model = audience_models.get(audience_id)
    if not model:
        raise HTTPException(status_code=404, detail='Аудитория не найдена')

    end_date = start_date + timedelta(days=6)
    
    # Получаем все потенциально релевантные события
    query = select(model).where(
        or_(
            # Неповторяющиеся события в диапазоне
            and_(
                model.repeat_frequency.is_(None),
                model.date >= start_date,
                model.date <= end_date
            ),
            # Повторяющиеся события, которые могли начаться до нашей недели
            and_(
                model.repeat_frequency.is_not(None),
                model.date <= end_date,
                or_(
                    model.repeat_until.is_(None),
                    model.repeat_until >= start_date
                )
            )
        )
    )
    
    result = await db.execute(query)
    events = result.scalars().all()
    
    # Обрабатываем события и вычисляем следующие даты
    response = []
    for event in events:
        if event.repeat_frequency:
            next_date = get_next_occurrence(
                event_date=event.date,
                repeat_frequency=event.repeat_frequency,
                repeat_until=event.repeat_until,
                week_start=start_date,
                week_end=end_date
            )
            
            if next_date:
                # Создаем копию события с обновленной датой
                event_data = event.__dict__.copy()
                event_data["date"] = next_date
                event_data["is_recurring"] = True  # Добавляем флаг повторения
                response.append(event_data)
        else:
            # Обычное событие
            event_data = event.__dict__.copy()
            event_data["is_recurring"] = False
            response.append(event_data)
    
    return response

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ScheduleResponse)
async def create_schedule(
    db: AsyncSession = Depends(get_db), 
    admin: models.User = Depends(oath2.require_role("admin"))):
    pass

@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_schedule(
    db: AsyncSession = Depends(get_db), 
    admin: models.User = Depends(oath2.require_role("admin"))):
    
    pass

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_schedule(
    db: AsyncSession = Depends(get_db), 
    admin: models.User = Depends(oath2.require_role("admin"))):
    
    pass

