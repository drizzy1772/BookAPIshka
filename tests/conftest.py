
import asyncio
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.database import Base, get_db
from app.main import app
from app.models import UserRole
from app.security import create_access_token, get_password_hash


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest.fixture
async def test_user(db_session: AsyncSession):
    from app.models import User

    user = User(
        username="testuser",
        email="test@example.com",
        password=get_password_hash("testpass123"),
        role=UserRole.USER,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
async def admin_user(db_session: AsyncSession):
    from app.models import User

    user = User(
        username="admin",
        email="admin@example.com",
        password=get_password_hash("adminpass123"),
        role=UserRole.ADMIN,
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
def user_token(test_user):
    return create_access_token({"sub": str(test_user.id)})

@pytest.fixture
def admin_token(admin_user):
    return create_access_token({"sub": str(admin_user.id)})

@pytest.fixture
async def test_author(db_session: AsyncSession):
    from datetime import date

    from app.models import Author

    author = Author(
        name='Test Author',
        bio='Bio',
        birth_date=date(1980, 1, 1)
    )
    db_session.add(author)
    await db_session.commit()
    await db_session.refresh(author)
    return author

@pytest.fixture
async def test_book(db_session: AsyncSession, test_author):
    from app.models import Book

    book = Book(
        title='Title Book',
        description='Description',
        price=2000,
        stock_quantity=16,
        author_id=test_author.id
    )
    db_session.add(book)
    await db_session.commit()
    await db_session.refresh(book)
    return book