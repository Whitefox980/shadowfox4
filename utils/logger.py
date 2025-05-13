from datetime import datetime

def log_info(message):
    print(f"[{timestamp()}] [OPERATER] [INFO] {message}")

def log_error(message):
    print(f"[{timestamp()}] [OPERATER] [ERROR] {message}")

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
