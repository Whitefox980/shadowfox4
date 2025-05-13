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
        self.history.append(scan_data)
        self.save()

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.history, f, indent=2)

    def get_all_missions(self):
        return self.history

    def get_last_mission(self):
        return self.history[-1] if self.history else None

    def evolve_strategy(self):
        if not self.history:
            return {"note": "Nema prethodnih misija za analizu."}

        module_stats = {}
        for mission in self.history:
            for module_name, result in mission.items():
                if module_name not in module_stats:
                    module_stats[module_name] = 0
                if isinstance(result, dict) and result.get("success"):
                    module_stats[module_name] += 1

        sorted_modules = sorted(module_stats.items(), key=lambda x: x[1], reverse=True)
        return {"prioritet_moduli": sorted_modules}
