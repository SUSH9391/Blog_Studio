import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from main import app, get_db
from database import Base
from models import User
from auth import hash_password

# Sync test DB for integration tests
SQLALCHEMY_DATABASE_URL_TEST = "sqlite+aiosqlite:///./test.db"
engine_test = create_async_engine(
    SQLALCHEMY_DATABASE_URL_TEST,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine_test, class_=AsyncSession)

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="function")
async def db_session():
    # Create tables
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        await session.close()
        # Drop tables after test
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def seeded_user(db_session):
    user = User(
        email="sushmitha@example.com",
        username="sushmitha",
        password_hash=hash_password("abc123@$")
    )
    db_session.add(user)
    await db_session.commit()
    return user
