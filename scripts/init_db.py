import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 匯入你的 Base
from app.models import Base

# 加載環境變數
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', '.env.prod'))
load_dotenv(dotenv_path=env_path)

def get_database_url() -> str:
    """動態生成資料庫 URL"""
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS", "")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    if DB_PASS:
        return f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return f"mysql+aiomysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async def init_db():
    """初始化資料庫"""
    database_url = get_database_url()
    engine = create_async_engine(
        database_url,
        echo=True,  # 可根據需要切換 SQL 語句輸出
        pool_pre_ping=True
    )

    async with engine.begin() as conn:
        print("創建資料庫表...")

        # 使用 Base.metadata.create_all 創建所有表
        await conn.run_sync(Base.metadata.create_all)

        print("資料庫表創建完成！")

    # 關閉引擎
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())
