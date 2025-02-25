import logging
import uuid
import os
from datetime import datetime
from threading import RLock
from colorama import Fore, Style, init
import json
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

init(autoreset=True)

# 定義自訂級別數值（介於 INFO 和 WARNING 之間）
SUCCESS_LEVEL_NUM = 25

# 註冊自訂級別名稱
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")

# 為 Logger 類別新增 success 方法
def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kwargs)

logging.Logger.success = success

class LogManager:
    _instance = None
    _lock = RLock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:  # 雙重檢查鎖定，確保只有一個實例
                    cls._instance = super(LogManager, cls).__new__(cls)
                    cls._instance.__initialized = False
        return cls._instance

    def __init__(self, log_dir: str = "logs/", max_bytes: int = 10 * 1024 * 1024, backup_count: int = 0):
        if self.__initialized:
            return  # 如果已初始化過，直接返回
        self.__initialized = True

        self.level_colors = {
            "success": Fore.GREEN,
            "error": Fore.RED,
            "warning": Fore.YELLOW,
            "info": Fore.WHITE,
            "debug": Fore.CYAN,
        }
        
        log_format = (
            "%(asctime)s | %(levelname)s | %(worker)s | %(task_id)s | "
            "%(process_id)s | %(process_time)s | %(status)s | %(method)s | "
            "%(router)s | %(params)s | %(log_message)s"
        )

        # 設置絕對路徑為 app/logs/
        base_dir = os.path.dirname(os.path.abspath(__file__))  # 獲取當前檔案所在目錄
        log_dir = os.path.join(base_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)

        # 生成當月的日誌檔案名稱
        current_month = datetime.now().strftime("%Y%m")
        log_file = os.path.join(log_dir, f"server-{current_month}.log")

        # 使用 RotatingFileHandler，按大小和月份切分
        self.rotating_handler = RotatingFileHandler(
            log_file, mode="a", maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        self.rotating_handler.setLevel(logging.INFO)
        self.rotating_handler.setFormatter(logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S"))

        # 初始化 logger
        self.logger = logging.getLogger("LogManager")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.rotating_handler)

        # 單獨的控制台處理器（帶顏色）
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)


    def log(self, level: str = "info", worker: str = "N/A", task_id: str = "N/A", process_id: str = "N/A", process_time: str = "N/A", status: str = "N/A", method: str = "N/A", router: str = "N/A", params=None, message: str = None):
        """
        打印結構化日誌到控制台，並記錄到日誌文件。
        :param level: 日誌級別（如 "success", "failure", "warning", "info", "debug"）。
        :param worker: Worker 名稱（默認為 "N/A"）。
        :param task_id: 任務 ID（默認為 "N/A"）。
        :param process_time: 任務處理時間（默認為 "N/A"）。
        :param status: HTTP 狀態碼（默認為 200）。
        :param method: 調用的方法名稱（默認為 "N/A"）。
        :param router: 調用的 API 路由（默認為 "N/A"）。
        :param params: 任務參數（默認為 None）。
        :param message: 任務訊息（默認為 None）。
        """
        with self._lock:
            # 處理 params
            if params is None:
                formatted_params = "None"
            else:
                try:
                    formatted_params = json.dumps(params, ensure_ascii=False, separators=(",", ":"))
                except (TypeError, ValueError):
                    formatted_params = str(params)

            process_id = str(uuid.uuid4())[:8] if process_id == "N/A" else process_id

            # 構建 extra 字段，用於 logger 格式化輸出
            extra = {
                "worker": worker,
                "task_id": task_id,
                "process_id": process_id,
                "process_time": process_time,
                "status": status,
                "method": method,
                "router": router,
                "params": formatted_params,
                "log_message": message
            }

            # 顏色映射
            color = self.level_colors.get(level.lower(), Fore.WHITE)

            # 控制台顯示帶顏色的訊息
            print(f"{color}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {level.upper()} | {worker} | {task_id} | {process_id} | {process_time} | {status} | {method} | {router} | {formatted_params} | {message}{Style.RESET_ALL}")

            # 設置日誌級別並記錄
            level = level.lower()
            if level == "success":
                self.logger.success(message, extra=extra)
            elif level == "error":
                self.logger.error(message, extra=extra)
            elif level == "warning":
                self.logger.warning(message, extra=extra)
            elif level == "info":
                self.logger.info(message, extra=extra)
            elif level == "debug":
                self.logger.debug(message, extra=extra)
            else:
                self.logger.info(message, extra=extra)

