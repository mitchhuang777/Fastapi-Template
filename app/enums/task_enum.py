from enum import Enum

class TaskID(Enum):
    """
    定義所有任務的 ID 對應關係。
    """
    UNDEFINED = -1              # 未定義
    FINISH = 666                # 任務結束
    EXCEPTION = 999             # 例外處理

    # 資料庫相關任務 (100 ~ 199)
    DB_SETUP = 100              # 資料庫初始化
    DB_INSERT = 101             # 插入資料
    DB_UPDATE = 102             # 更新資料
    DB_DELETE = 103             # 刪除資料
    DB_QUERY = 104              # 查詢資料

    # FastAPI 相關任務 (200 ~ 299)
    FASTAPI_STARTUP = 200       # FastAPI 服務啟動
    FASTAPI_REQUEST = 201       # FastAPI 處理請求
    FASTAPI_SHUTDOWN = 202      # FastAPI 服務關閉
    FASTAPI_ERROR = 203         # FastAPI 錯誤處理

    # 資料抓取相關任務 (301 ~ 399)
    FETCH_STOCK_DATA = 301        # 抓取股票資訊
    FETCH_EXCHANGE_RATE = 302     # 抓取匯率資訊
    FETCH_ERROR = 303     # 處理抓取錯誤  

    # 排程相關任務 (401 ~ 499)
    SCHEDULE_TASK = 401         # 排程任務
    SCHEDULE_ERROR = 402        # 排程錯誤

    
