from .routers.example_router import router as sample_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(sample_router)
