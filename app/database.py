from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from dotenv import load_dotenv
import os

# 動態加載環境變數文件
ENV = os.getenv("ENV", "dev")  # 預設為開發環境
dotenv_file = f".env.{ENV}"  # 根據環境名稱動態選擇 .env 文件
load_dotenv(dotenv_path=dotenv_file)

# 從環境變數中讀取資料庫連接參數
def get_database_url() -> str:
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    # 驗證環境變數是否設置
    if not all([DB_HOST, DB_USER, DB_PASS, DB_PORT, DB_NAME]):
        raise ValueError("One or more required environment variables are missing. Please check .env.<ENV> file.")
    
    return f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 動態生成 DATABASE_URL
DATABASE_URL = get_database_url()

# 創建異步資料庫引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "False").lower() == "true",  # 根據環境變量動態開啟/關閉 SQL 日誌
    pool_pre_ping=True,  # 確保連接有效
    pool_recycle=1800,   # 回收閒置超過 30 分鐘的連接
)

# 創建一個 SessionLocal 類，用於生成資料庫連接
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 提供資料庫連接依賴
async def get_db() -> AsyncSession:
    """
    資料庫連接管理函數，適用於異步操作，生成資料庫連接並自動管理提交、回滾及關閉連接。
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # 提交資料變更
        except Exception as e:
            await session.rollback()  # 如果出現異常，回滾變更
            raise e
        finally:
            await session.close()  # 確保會話關閉

# 測試連線功能（可選）
async def test_connection():
    """
    測試資料庫連線是否成功。
    """
    try:
        async with engine.connect() as conn:
            # 使用 SQLAlchemy 的 text() 包裹原始 SQL 語句
            result = await conn.execute(text("SELECT 1"))
            print("Database connection successful! Test query result:", result.scalar())
    except Exception as e:
        print("Database connection failed:", str(e))
    finally:
        await engine.dispose()

# 如果需要在腳本模式下測試，可以取消以下註解
import asyncio
asyncio.run(test_connection())
