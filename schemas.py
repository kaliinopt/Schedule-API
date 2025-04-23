from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, time, datetime

date_of = date

class UserBase(BaseModel):
    username: str
    password: str

class ScheduleBase(BaseModel): 
    subject: str
    teacher: str
    start_time: time
    end_time: time
    repeat_frequency: Optional[str] = None
    repeat_until: Optional[date] = None

class ScheduleResponse(ScheduleBase):
    id: int
    date: date 
    
    class Config:
        from_attributes = True

class ScheduleCreate(ScheduleBase):
    audience_id: int
    date: date

class ScheduleUpdate(BaseModel):
    subject: Optional[str] = None
    teacher: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    date: Optional[date_of] = None
    repeat_frequency: Optional[str] = None
    repeat_until: Optional[date_of] = None

class UserLogin(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

class UserCreate(UserBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

@field_validator('start_time', 'end_time')
def validate_time_format(cls, v):
    if v.hour > 23 or v.minute > 59 or v.second > 59:
        raise ValueError("Некорректное время")
    return v