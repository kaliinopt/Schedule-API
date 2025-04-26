from sqlalchemy import Column, Integer, String, Time, Date
from .database import Base

# Базовый класс для всех аудиторий
class BaseClassRoom(Base):
    __abstract__ = True  # Указываем, что это абстрактный класс 
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    subject = Column(String, nullable=False)
    teacher = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    date = Column(Date, nullable=False)
    repeat_frequency = Column(String(50), nullable=True)
    repeat_until = Column(Date, nullable=True)