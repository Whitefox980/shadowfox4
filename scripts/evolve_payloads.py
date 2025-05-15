import json
import os
import sys, os
sys.path.insert(0, os.path.abspath("."))

from core.mutation_engine import MutationEngine

def load_history(path="data/fuzz_history.json"):
    if not os.path.exists(path):
        print("[EVOLVE] Nema fuzz istorije.")
        return {}
    with open(path) as f:
        return json.load(f)

def evolve(history):
    engine = MutationEngine()
    evolved_set = {}

    for attack_type, entries in history.items():
        successful = [e["payload"] for e in entries if e.get("success")]
        evolved = []

        for payload in successful:
            mutated = engine.mutate_payload(payload)
            evolved.extend(mutated)

        if evolved:
            evolved_set[attack_type] = evolved

    return evolved_set

def display(evolved):
    print("\n[EVOLVE] Sledeća generacija payload mutacija:\n")
    for typ, payloads in evolved.items():
        print(f"== {typ.upper()} ({len(payloads)} mutacija):")
        for p in payloads:
            print(f" - {p}")
        print()

if __name__ == "__main__":
    history = load_history()
    evolved = evolve(history)
    display(evolved)

    with open("data/evolved_payloads.json", "w") as f:
        json.dump(evolved, f, indent=2)
    print(f"[EVOLVE] Sačuvano {sum(len(v) for v in evolved.values())} mutacija u data/evolved_payloads.json")
