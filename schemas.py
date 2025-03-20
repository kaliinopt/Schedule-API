from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class ScheduleBase(BaseModel):
    subject: str
    teacher: str
    start_time: time
    end_time: time
    date_of: date
    repeat_frequency: Optional[str] = None
    repeat_until: Optional[date] = None

class ScheduleResponse(ScheduleBase):
    pass

    class Config:
        orm_mode = True