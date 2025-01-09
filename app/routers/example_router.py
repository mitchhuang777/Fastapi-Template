from fastapi import APIRouter

router = APIRouter()

@router.get("/sample")
async def get_sample_data():
    """
    簡單範例端點，返回靜態數據。
    """
    return {"message": "Hello, this is a sample response!"}
