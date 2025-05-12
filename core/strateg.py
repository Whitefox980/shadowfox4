import json
from core.ai_memory import AIMemory

class Strateg:
    def __init__(self, scan_path="data/scan_results.json"):
        with open(scan_path) as f:
            self.scan = json.load(f)
        self.memory = AIMemory()

    def generate_strategy(self):
        plan = {}
        used_modules = list(self.scan.keys())

        # Pamtimo sve što je bilo deo misije
        for mod in used_modules:
            for target, result in self.scan[mod].items():
                if isinstance(result, str) and "VULNERABLE" in result:
                    self.memory.record_success(mod)

        self.memory.remember_mission(self.scan)
        self.memory.save()

        # Koristi evoluciju da napravi novi plan
        top = self.memory.evolve_strategy()
        for mod in top[:5]:
            plan[mod] = [mod]  # Format da bude isti kao attack_plan

        return plan

# Pokretanje
if __name__ == "__main__":
    s = Strateg()
    strategy = s.generate_strategy()
    with open("data/next_plan.json", "w") as f:
        json.dump(strategy, f, indent=2)
    print("[STRATEG] Sledeći plan generisan u data/next_plan.json")
