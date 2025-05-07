from typing import AsyncGenerator
import pytest
from sqlalchemy import NullPool, insert
from app.database.database import Base, get_db
from main import app
from app.core.config import load_config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from app.core.utils import hash

Config = load_config()

DB_URL = Config.TEST_DATABASE_URL

test_engine = create_async_engine(
        url=DB_URL,
        echo=False,
        poolclass=NullPool,
        connect_args={"command_timeout": 5}
    )
    

@pytest.fixture(scope="session")
def event_loop():
    """Переопределяем event loop для pytest-asyncio"""
    import asyncio
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


#create a session to override the default db session
async def test_get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(class_=AsyncSession, expire_on_commit=False)
    try:
        async with Session(bind=test_engine) as session:
            yield session
    finally:
        await session.close()
        
@pytest_asyncio.fixture(scope='function')
async def client():
    async with test_engine.begin() as conn:
        from app.database.models import User
        await conn.run_sync(Base.metadata.create_all)

    # override the session
    app.dependency_overrides[get_db] = test_get_session
    
    async with AsyncClient(timeout=5, transport=ASGITransport(app=app), base_url="https://test") as client:
        yield client



@pytest_asyncio.fixture(scope='session')
async def create_test_admin():
    """Фикстура создаёт тестового админа один раз перед всеми тестами."""
    admin_data = {
        "username": "test_admin",
        "password": hash("adminpass123"),
        "role": "admin",
    }
    
    # Вставляем админа напрямую в БД
    from app.database.models import User
    stmt = insert(User).values(**admin_data)
    async with test_engine.begin() as conn:
        await conn.execute(stmt)
        await conn.commit()


@pytest_asyncio.fixture(scope='function')
async def close_():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    app.dependency_overrides.clear()


