import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event, JSON, TypeDecorator, String
from sqlalchemy.dialects import sqlite
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from app.db.base import Base, get_db
from app.main import app
from app.core.config import settings
import uuid as uuid_pkg

# Custom UUID type that works with both PostgreSQL and SQLite
class UUID(TypeDecorator):
    """Platform-independent UUID type.
    Uses PostgreSQL's UUID type, otherwise uses String(36).
    """
    impl = String(36)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            if isinstance(value, uuid_pkg.UUID):
                return str(value)
            return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid_pkg.UUID):
            try:
                return uuid_pkg.UUID(value)
            except (ValueError, AttributeError):
                # If value is not a valid UUID string, return as-is
                return value
        return value

# Use an in-memory SQLite database for speed and isolation
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Register SQLite-compatible types for PostgreSQL-specific types
@event.listens_for(Base.metadata, "before_create")
def _set_sqlite_pragma(target, connection, **kw):
    """Configure SQLite to work with PostgreSQL types"""
    if connection.dialect.name == "sqlite":
        # Replace JSONB with JSON for SQLite
        for table in target.tables.values():
            for column in table.columns:
                # Check for JSONB type
                if isinstance(column.type, JSONB):
                    column.type = JSON()
                # Check for PostgreSQL UUID type (multiple ways to check)
                type_name = column.type.__class__.__name__
                if type_name == 'UUID' or isinstance(column.type, PG_UUID):
                    column.type = UUID()

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Create a fresh database for each test function."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback() # Rollback after test
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """Create a test client that uses the test database."""
    from httpx import ASGITransport
    
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    
    app.dependency_overrides.clear()
