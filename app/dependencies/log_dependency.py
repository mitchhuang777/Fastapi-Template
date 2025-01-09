from app.log_manager import LogManager

# 創建一個 LogManager 的單例實例
log_manager = LogManager()

def get_log_manager():
    """
    提供 LogManager 實例的依賴項，供 FastAPI 的依賴注入使用。
    """
    return log_manager
