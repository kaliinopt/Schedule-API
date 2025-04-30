from . import models, schemas, oath2
from . import check_time_conflicts, get_next_occurrence_by_week
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from . import get_db
from typing import List, Type
from datetime import date, timedelta
import logging

loger = logging.getLogger("app")

#Захардкодил по причине неизменности аудиторий
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

async def get_audience_model(audience_id: int):
    model = audience_models.get(audience_id)
    if not model:
        raise HTTPException(status_code=404, detail="Аудитория не найдена")
    return model


@router.get("/{audience_id}/{date}", response_model=List[schemas.ScheduleResponse])
async def get_schedule_for_date(
    date: date,
    model: Type[models.BaseClassRoom] = Depends(get_audience_model),
    db: AsyncSession = Depends(get_db)):
    """Получение расписания на день, удалю если не понадобиться"""
    schedule = await db.execute(
        select(model).where(model.date == date)
    )
    
    return schedule.scalars().all()

@router.get("/{audience_id}/week/{start_date}", response_model=List[schemas.ScheduleResponse])
async def get_week_schedule(
    start_date: date,
    model: Type[models.BaseClassRoom] = Depends(get_audience_model),
    db: AsyncSession = Depends(get_db)):
    """Получение расписания на неделю"""

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
            next_date = get_next_occurrence_by_week(
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
    schedule: schemas.ScheduleCreate,
    db: AsyncSession = Depends(get_db), 
    admin: models.User = Depends(oath2.require_role("admin"))):
    """Создание расписания"""

    model = audience_models.get(schedule.audience_id)
    if not model:
        raise HTTPException(status_code=404, detail="Аудитория не найдена")

    
    await check_time_conflicts(db, model, schedule)

    schedule_db = model(**schedule.model_dump(exclude={"audience_id"}))
    db.add(schedule_db)
    await db.commit()
    await db.refresh(schedule_db)
    return schedule_db

@router.put("/{audience_id}/{id}", response_model=schemas.ScheduleResponse)
async def update_schedule(
    id: int,
    update_schedule: schemas.ScheduleUpdate,
    model: Type[models.BaseClassRoom] = Depends(get_audience_model),
    db: AsyncSession = Depends(get_db), 
    admin: models.User = Depends(oath2.require_role("admin"))):
    """Обновление конкретного события"""
    
    event = await db.get(model, id)
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    
    if any(field in update_schedule.model_dump(exclude_unset=True) 
        for field in ["start_time", "end_time", "date"]):
            await check_time_conflicts(db, model, update_schedule, exclude_event_id=id)
    
    for field, value in update_schedule.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    
    await db.commit()
    await db.refresh(event)
    return event

@router.delete("/{audience_id}/{id}")
async def delete_schedule(
    id: int,
    model: Type[models.BaseClassRoom] = Depends(get_audience_model),
    db: AsyncSession = Depends(get_db), 
    admin: models.User = Depends(oath2.require_role("admin"))):
    """Удаление конкретного события"""
    
    event = await db.get(model, id)

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Событие не найдено")
    
    await db.delete(event)
    await db.commit()
    loger.info(f"Была удалена запись с id: {event.id} из таблицы {model.__tablename__} с аккаунта {admin.username}")
    return {"message": "Успешно удалено"}

