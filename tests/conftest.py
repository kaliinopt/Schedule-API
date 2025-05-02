import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from main import app
from app.database.database import Base, get_db
from app.core.config import load_config
from app.database.models import User

# Загрузка конфигурации
config = load_config()

@pytest_asyncio.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        config.TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool,
        connect_args={"command_timeout": 3}
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture
async def db_session(engine):
    async with async_sessionmaker(
        engine,
        expire_on_commit=False,
        autoflush=False
    )() as session:
        async with session.begin():
            yield session

@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
            yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        timeout=3.0,
        follow_redirects=True
    ) as client:
        yield client
    
    app.dependency_overrides.clear()