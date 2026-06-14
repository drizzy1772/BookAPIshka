import asyncio
from sqlalchemy import text
from app.database import engine

async def clean_db():
    async with engine.begin() as conn:
        # Удаляем все таблицы
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
        print("База данных очищена!")

asyncio.run(clean_db())