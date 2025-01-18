# 使用官方的 Python 基礎映像
FROM python:3.10-slim

# 設置工作目錄
WORKDIR /app

# 安裝系統依賴工具、MySQL Server 和其他必要工具
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev-compat \
    libmariadb-dev \
    default-mysql-server \
    tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 設置時區
ENV TZ=Asia/Taipei

# 複製依賴文件並安裝 Python 包
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式源碼
COPY . .

# 開放端口（FastAPI 默認 8000）
EXPOSE 8000

# 啟動 MySQL 並運行應用程式
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
