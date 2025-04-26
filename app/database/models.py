from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base
from .base_models import BaseClassRoom

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))

# Конкретные классы для каждой аудитории, аудитории не меняются
class Class_142(BaseClassRoom):
    __tablename__ = 'class_142'

class Class_143(BaseClassRoom):
    __tablename__ = 'class_143'

class Class_251(BaseClassRoom):
    __tablename__ = 'class_251'

class Class_252(BaseClassRoom):
    __tablename__ = 'class_252'

class Class_253(BaseClassRoom):
    __tablename__ = 'class_253'

class Class_254(BaseClassRoom):
    __tablename__ = 'class_254'

class Class_255(BaseClassRoom):
    __tablename__ = 'class_255'

class Class_339(BaseClassRoom):
    __tablename__ = 'class_339'

class Class_340(BaseClassRoom):
    __tablename__ = 'class_340'

class Class_341(BaseClassRoom):
    __tablename__ = 'class_341'

class Class_342(BaseClassRoom):
    __tablename__ = 'class_342'

class Class_343(BaseClassRoom):
    __tablename__ = 'class_343'
    