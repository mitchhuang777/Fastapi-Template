from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.config.global_settings import log_manager
from app.services.sample_service import async_sample_service
from app.enums.task_enum import TaskID
from app.database import AsyncSessionLocal
import asyncio
import uuid

scheduler = AsyncIOScheduler()
worker = "scheduler"

async def fetch_sample_data():
    """定時任務：抓取並存儲今日分鐘匯率"""
    process_id = str(uuid.uuid4())[:8]

    async with AsyncSessionLocal() as db:
        try:
            await async_sample_service(db)
        except Exception as e:
            # 在這裡處理異常情況，例如記錄日誌
            log_manager.log(
                level="error",
                worker=worker,
                task_id=TaskID.SCHEDULE_ERROR.value,
                process_id=process_id,
                message=f"定時任務執行失敗：{e}"
            )

def add_jobs():
    """添加定時任務到調度器"""

    # 周一到周五，9:00 至 18:00，每 30 分鐘執行一次
    scheduler.add_job(
        func=fetch_sample_data,
        trigger=CronTrigger(day_of_week="mon-fri", hour="9-18", minute="0,30"),
        id="fetch_stock_data_30m",
        replace_existing=True
    )

async def start_scheduler():
    """啟動調度器"""
    process_id = str(uuid.uuid4())[:8]
    
    
    scheduler.start()
    log_manager.log(
        level="info",
        worker=worker,
        task_id=TaskID.SCHEDULE_TASK.value,
        process_id=process_id,
        message="啟動排程器..."
    )

    add_jobs()
    scheduler.print_jobs()
    await asyncio.Future()

# 如果需要在主程序中啟動：
if __name__ == "__main__":
    # 使用 asyncio.run 啟動調度器
    asyncio.run(start_scheduler())