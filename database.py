from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from config import DATABASE_LOGIN, DATABASE_PASSWORD, POSTGRES_SERVER, POSTGRES_PORT

Base = declarative_base()

SQLALCHEMY_DATABASE_URL_SYNC = f'postgresql://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{DATABASE_LOGIN}'

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{DATABASE_LOGIN}'

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