import json
from collections import defaultdict, Counter
import os

class AIMemory:
    def __init__(self, path="data/agent_brain.json"):
        self.path = path
        if os.path.exists(path):
            with open(path) as f:
                self.mem = json.load(f)
        else:
            self.mem = {"success": defaultdict(int), "history": []}

    def record_success(self, module_name):
        self.mem["success"][module_name] += 1

    def remember_mission(self, scan_result):
        self.mem["history"].append(scan_result)

    def evolve_strategy(self):
        ranked = Counter(self.mem["success"]).most_common()
        return [mod for mod, _ in ranked]

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.mem, f, indent=2)

# Korišćenje (iz shadow_agent.py, npr.)
# mem = AIMemory()
# mem.record_success("SQL Injection Fuzzer")
# mem.remember_mission(full_scan_result_dict)
# mem.save()
