import datetime
import os

LOG_PATH = "data/logs/shadowfox.log"

def log(agent, message, status="info"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{agent.upper()}] [{status.upper()}] {message}\n"

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(line)

    print(line.strip())
