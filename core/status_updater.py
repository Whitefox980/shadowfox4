import json
import os
from datetime import datetime

def update_agent_status(agent_name, target, action):
    path = "data/agent_status.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            status_data = json.load(f)
    else:
        status_data = {}

    status_data[agent_name] = {
        "target": target,
        "activity": "Active",
        "last_action": action,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(path, "w") as f:
        json.dump(status_data, f, indent=2)
