import json
import os
from datetime import datetime

def archive_mission(target, vulns_found, modules_used):
    path = "data/mission_history.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            history = json.load(f)
    else:
        history = []

    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target": target,
        "vulns": vulns_found,
        "modules": modules_used
    }

    history.append(new_entry)

    with open(path, "w") as f:
        json.dump(history, f, indent=2)
