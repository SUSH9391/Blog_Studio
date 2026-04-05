from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings

# Lazy engine/session creation for Alembic compat (avoids global create_async_engine)
engine = None
AsyncSessionLocal = None
sync_engine = None

def init_db():
    global engine, AsyncSessionLocal
    if engine is None:
        from urllib.parse import urlparse, parse_qs, urlencode
        parsed = urlparse(settings.database_url)
        query_dict = dict(parse_qs(parsed.query))
        query_dict.pop('sslmode', None)
        clean_query = urlencode(query_dict, doseq=True)
        clean_url = parsed._replace(query=clean_query).geturl()
        engine = create_async_engine(clean_url)
        AsyncSessionLocal = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

def init_sync_db():
    global sync_engine
    if sync_engine is None:
        sync_url = settings.database_url.replace('postgresql+asyncpg://', 'postgresql+psycopg2://')
        sync_engine = create_engine(sync_url)

class Base(DeclarativeBase):
    pass


async def get_db():
    init_db()
    async with AsyncSessionLocal() as session:
        yield session
