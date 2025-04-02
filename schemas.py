from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime

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
    date: date 
    
    class Config:
        from_attributes = True
    pass

    class Config:
        from_attributes = True

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