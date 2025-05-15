import os
import json
from datetime import datetime

class MissionMemory:
    def __init__(self, log_dir="data/mission_logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

    def remember_mission(self, mission_data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.log_dir}/mission_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(mission_data, f, indent=4)
        print(f"[MEMORY] Misija zabeležena u: {filename}")
