from .routers.example_router import sample_router
from fastapi import FastAPI
from app.scheduler import start_scheduler, scheduler
from app.config.global_settings import log_manager
import asyncio

app = FastAPI()

app.include_router(sample_router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_scheduler())  # 啟動排程器

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown(wait=False)  # 關閉排程器