import json, os
from core.memory import MissionMemory
class Strateg:
    def __init__(self):
        self.memory = MissionMemory()
        scan_path = "data/scan_results.json"
        if not os.path.exists(scan_path):
            with open(scan_path, "w") as f:
                json.dump({}, f)
        with open(scan_path) as f:
            self.results = json.load(f)
    def generate_strategy(self, results):
        self.scan = results
        used_modules = list(self.scan.keys())
    # (ostatak tvoje logike za mutacije ili strategiju)
        plan = {}

        # Pamtimo sve što je bilo deo misije
        for mod in used_modules:
            for target, result in self.scan[mod].items():
                if isinstance(result, str) and "VULNERABLE" in result:
                    self.memory.record_success(mod)

        self.memory.remember_mission(self.scan)
        self.memory.save()

        # Koristi evoluciju da napravi novi plan
        top = self.memory.evolve_strategy()
        print("[STRATEG] Top moduli iz prethodnih misija:")
        plan = {}
        for mod, count in top.get("prioritet_moduli", [])[:5]:
            print(f" - {mod}: {count} uspešnih pogodaka")
            plan[mod] = [mod]  # Format da bude isti kao attack_plan

        return plan

# Pokretanje
if __name__ == "__main__":
    s = Strateg()
    strategy = s.generate_strategy()
    with open("data/next_plan.json", "w") as f:
        json.dump(strategy, f, indent=2)
    print("[STRATEG] Sledeći plan generisan u data/next_plan.json")
