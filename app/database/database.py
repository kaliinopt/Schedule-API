from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import load_config

config = load_config()

Base = declarative_base()

engine = create_async_engine(config.SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
        bind=engine, 
        class_=AsyncSession, 
        expire_on_commit=False
        )

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db