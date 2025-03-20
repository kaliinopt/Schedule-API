from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
SQLALCHEMY_DATABASE_URL_SYNC = 'postgresql://postgres:genby,ehu4@192.168.201.20:5432/postgres'

SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://postgres:genby,ehu4@192.168.201.20:5432/postgres'

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