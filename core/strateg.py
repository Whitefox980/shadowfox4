import json, os
from core.memory import MissionMemory
class Strateg:
    def __init__(self):
        self.scan = {}

    def generate_strategy(self, results):
        for mod in results:
            if not isinstance(results[mod], dict):
                print(f"[STRATEG] Preskačem modul {mod} jer nije dict (tip: {type(results[mod])})")
                continue

            for payload, response in results[mod].items():
                if "VULNERABLE" in str(response):
                    print(f"[STRATEG] Otkriveno: {mod} -> {payload}")
                # Ovde dodaj AI učenje u budućnosti
# Pokretanje
if __name__ == "__main__":
    s = Strateg()
    strategy = s.generate_strategy()
    with open("data/next_plan.json", "w") as f:
        json.dump(strategy, f, indent=2)
    print("[STRATEG] Sledeći plan generisan u data/next_plan.json")
