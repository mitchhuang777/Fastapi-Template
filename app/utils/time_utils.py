from datetime import datetime

def calculate_process_time(start_time: datetime) -> str:
    """
    計算處理時間，並根據時間長度自動切換單位（ms 或 s）。
    :param start_time: 起始時間（datetime 格式）
    :return: 帶單位的處理時間字串（例如 "850.12 ms" 或 "1.28 s"）
    """
    process_time_ms = (datetime.now() - start_time).total_seconds() * 1000
    if process_time_ms < 1000:
        return f"{process_time_ms:.2f} ms"
    else:
        return f"{process_time_ms / 1000:.2f} s"
