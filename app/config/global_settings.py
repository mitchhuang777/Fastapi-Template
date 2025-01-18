import os
from app.log_manager import LogManager

# 設置專案根目錄 BASE_DIR 為 app/ 目錄
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 使用固定日誌路徑初始化 LogManager
log_manager = LogManager()
