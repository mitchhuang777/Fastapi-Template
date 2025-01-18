import uuid
from app.config.global_settings import log_manager
from sqlalchemy.ext.asyncio import AsyncSession


worker = "services"

async def async_sample_service(db: AsyncSession):
    """示例服務"""

