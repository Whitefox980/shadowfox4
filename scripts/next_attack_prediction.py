import json
import os

def load_history(path="data/fuzz_history.json"):
    if not os.path.exists(path):
        print("[PREDIKTOR] Nema fuzz istorije.")
        return {}

    with open(path) as f:
        return json.load(f)

def predict(history):
    best_module = None
    best_rate = 0

    for attack_type, attempts in history.items():
        total = len(attempts)
        if total == 0:
            continue
        success = sum(1 for x in attempts if x.get("success"))
        rate = success / total

        if rate > best_rate:
            best_module = attack_type
            best_rate = rate

    return best_module, round(best_rate * 100, 2)

if __name__ == "__main__":
    history = load_history()
    module, rate = predict(history)

    if module:
        print(f"\n[PREDIKTOR] Najuspešniji modul za sledeću misiju:")
        print(f" >> {module.upper()} sa uspešnošću od {rate}%\n")
    else:
        print("[PREDIKTOR] Nema dovoljno podataka za predikciju.")
