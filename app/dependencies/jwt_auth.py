import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from pathlib import Path

# 載入環境變數
base_dir = Path(__file__).resolve().parent.parent  # 指向 app/
env_path = base_dir / ".env.dev"
load_dotenv(env_path)

# 配置秘鑰與算法
SECRET_KEY = os.getenv("FAST_API_SECRET_KEY")  # 若未設置則提供默認值
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token 默認過期時間為 30 分鐘

# FastAPI 認證方案
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    生成 JWT Token，包含過期時間。
    
    :param data: 要編碼的數據 (如用戶信息)。
    :param expires_delta: 過期時間，若未提供則使用默認值。
    :return: 生成的 JWT Token 字符串。
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    """
    驗證 JWT Token 的合法性與有效性。
    
    :param token: 待驗證的 JWT Token。
    :return: 解碼後的數據 (字典形式)。
    :raises HTTPException: 若驗證失敗則拋出 401 錯誤。
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    從 Bearer Token 中提取並驗證當前用戶。
    
    :param credentials: FastAPI 自動提取的 Bearer Token 憑證。
    :return: 解碼後的數據 (如用戶信息)。
    """
    token = credentials.credentials
    return verify_access_token(token)
