from passlib.context import CryptContext
from app.api.schemas.schemas import ScheduleCreate
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import BaseClassRoom
from fastapi import HTTPException
from sqlalchemy import select, and_, or_
from typing import Optional, List
from datetime import date, timedelta, time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Делает хеш
def hash(password: str):
    return pwd_context.hash(password)


# Проверка подлинности
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Input should be a valid date in format YYYY-MM-DD
def get_next_occurrence_by_week(
    event_date: date,
    repeat_frequency: Optional[str],
    repeat_until: Optional[date],
    week_start: date,
    week_end: date,
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


def calculate_recurring_dates(
    start_date: date,
    repeat_frequency: str,
    repeat_until: Optional[date],
    check_from: date,
    check_to: date,
) -> List[date]:
    """
    Вычисляет все даты повторений события в заданном диапазоне.

    Args:
        start_date: Дата первого события
        repeat_frequency: Тип повторения ('daily', 'weekly', 'secondweek', 'monthly')
        repeat_until: Дата окончания повторений (None если неизвестно, ограничение 180 дней)
        check_from: Начало проверяемого периода
        check_to: Конец проверяемого периода

    Returns:
        Список дат, когда событие повторяется в проверяемом периоде
    """
    dates = []
    current_date = start_date
    max_iterations = 365 * 5  # Защита от бесконечного цикла (5 лет)

    for _ in range(max_iterations):
        # Если текущая дата уже после проверяемого периода
        if current_date > check_to:
            break

        # Если текущая дата в проверяемом периоде и до repeat_until
        if current_date >= check_from and (
            repeat_until is None or current_date <= repeat_until
        ):
            dates.append(current_date)

        # Переходим к следующей дате повторения
        if repeat_frequency == "daily":
            current_date += timedelta(days=1)
        elif repeat_frequency == "weekly":
            current_date += timedelta(weeks=1)
        elif repeat_frequency == "secondweek":
            current_date += timedelta(weeks=2)
        elif repeat_frequency == "monthly":
            # Добавляем 1 месяц, корректируя день если нужно
            if current_date.month == 12:
                next_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                next_date = current_date.replace(month=current_date.month + 1)

            # Корректируем день если в следующем месяце его нет
            try:
                current_date = next_date.replace(day=start_date.day)
            except ValueError:
                current_date = next_date.replace(day=28)  # Безопасный день
        else:
            break

    return dates


def check_time_overlap(
    time1_start: time, time1_end: time, time2_start: time, time2_end: time
) -> bool:
    """Проверяет пересечение двух временных интервалов"""
    return not (time1_end <= time2_start or time2_end <= time1_start)


async def check_recurring_conflicts(
    db: AsyncSession,
    model: Type[BaseClassRoom],
    new_event: ScheduleCreate,
    exclude_event_id: Optional[int] = None,
) -> None:
    """
    Проверяет пересечения нового события со всеми повторяющимися событиями
    """
    # Определяем период для проверки, задаем диапазон в 180 дней
    check_from = new_event.date
    check_to = (
        new_event.repeat_until
        if new_event.repeat_until
        else new_event.date + timedelta(days=180)
    )

    conditions = [
        model.repeat_frequency.is_not(None),
        or_(model.repeat_until.is_(None), model.repeat_until >= check_from),
    ]

    if exclude_event_id is not None:
        conditions.append(model.id != exclude_event_id)

    # Находим все повторяющиеся события в этой аудитории
    query = select(model).where(and_(*conditions))
    existing_events = (await db.execute(query)).scalars().all()

    for event in existing_events:
        # Получаем все даты повторений существующего события в нашем периоде
        event_dates = calculate_recurring_dates(
            start_date=event.date,
            repeat_frequency=event.repeat_frequency,
            repeat_until=event.repeat_until,
            check_from=check_from,
            check_to=check_to,
        )

        # Проверяем каждую дату на пересечение по времени
        for event_date in event_dates:
            if event_date == new_event.date or (
                new_event.repeat_frequency
                and calculate_recurring_dates(
                    start_date=new_event.date,
                    repeat_frequency=new_event.repeat_frequency,
                    repeat_until=new_event.repeat_until,
                    check_from=event_date,
                    check_to=event_date,
                )
            ):

                if check_time_overlap(
                    event.start_time,
                    event.end_time,
                    new_event.start_time,
                    new_event.end_time,
                ):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Пересечение с повторяющимся событием (ID: {
                            event.id}, дата: {event_date})",
                    )


# Проверка на конфликты времени
async def check_time_conflicts(
    db: AsyncSession,
    model: Type[BaseClassRoom],
    new_event: ScheduleCreate,
    exclude_event_id: Optional[int] = None,
) -> None:
    """Проверяет все возможные конфликты времени"""
    if new_event.start_time >= new_event.end_time:
        raise HTTPException(
            status_code=400, detail="Конечное время должно быть позже начального"
        )

    conditions = [
        model.date == new_event.date,
        model.start_time < new_event.end_time,
        model.end_time > new_event.start_time,
    ]

    if exclude_event_id is not None:
        conditions.append(model.id != exclude_event_id)

    # Проверка обычных событий
    query = select(model).where(and_(*conditions))
    if (await db.execute(query)).scalars().first():
        raise HTTPException(status_code=400, detail="Пересечение времени")

    # Проверка повторяющихся событий
    await check_recurring_conflicts(db, model, new_event, exclude_event_id)
