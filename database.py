from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from config import LOGIN_DATABASE, PASSWORD_DATABASE


Base = declarative_base()

SQLALCHEMY_DATABASE_URL_SYNC = f'postgresql://{LOGIN_DATABASE}:{PASSWORD_DATABASE}@192.168.201.20:5432/postgres'

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{LOGIN_DATABASE}:{PASSWORD_DATABASE}@192.168.201.20:5432/postgres'

sync_engine = create_engine(SQLALCHEMY_DATABASE_URL_SYNC)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
        bind=engine, 
        class_=AsyncSession, 
        expire_on_commit=False
        )

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db