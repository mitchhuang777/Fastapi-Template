import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.database import get_db, engine
import asyncio
from app.services.sample_service import async_sample_service
from sqlalchemy.ext.asyncio import AsyncSession

async def main():
    try:
        async for db in get_db():  
            await async_sample_service(db)
    finally:
        await engine.dispose()  # 確保釋放資料庫連接池

if __name__ == "__main__":
    asyncio.run(main())
