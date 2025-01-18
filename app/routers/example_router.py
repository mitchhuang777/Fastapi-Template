from fastapi import APIRouter
from app.database import get_db
from app.dependencies.log_dependency import get_log_manager
from app.log_manager import LogManager
from app.utils.time_utils import calculate_process_time
from app.schemas.sample import SampleResponse
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

sample_router = APIRouter()

@sample_router.get("/sample", response_model=SampleResponse)
async def get_sample_data(
    db: AsyncSession = Depends(get_db),
    log_manager: LogManager = Depends(get_log_manager)
):
    """
    簡單範例端點，返回靜態數據。
    """
    return SampleResponse(
        message="Hello, World!"
    )