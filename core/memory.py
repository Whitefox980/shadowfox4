import json
import os

class MissionMemory:
    def __init__(self, path="data/mission_history.json"):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)
        with open(self.path) as f:
            self.history = json.load(f)
    def remember_mission(self, scan_data):
        target = scan_data.get("target", "unknown_target")
    
        if target not in self.history:
            self.history[target] = []

            self.history[target].append(scan_data)

        with open(self.path, "w") as f:
            json.dump(self.history, f, indent=2)
    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.history, f, indent=2)

    def get_all_missions(self):
        return self.history

    def get_last_mission(self):
        return self.history[-1] if self.history else None

    def evolve_strategy(self):
        scores = {}

        for mission_list in self.history.values():
            for mission in mission_list:
                if isinstance(mission, dict):
                    for module_name, result in mission.items():
                        if module_name not in scores:
                            scores[module_name] = 0
                        if isinstance(result, dict) and result.get("success"):
                            scores[module_name] += 1

    # Sortiramo top 5 po uspehu
        top_modules = sorted(scores, key=scores.get, reverse=True)
        return top_modules[:5]
