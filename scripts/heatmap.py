import json
import os

def load_history(path="data/fuzz_history.json"):
    if not os.path.exists(path):
        print("[HEATMAP] Nema fuzz istorije.")
        return {}
    with open(path) as f:
        return json.load(f)

def display_heatmap(data):
    print("\n[HEATMAP] Uspešnost AI napada po tipu:\n")
    for attack_type, entries in data.items():
        total = len(entries)
        if total == 0:
            continue
        success = sum(1 for e in entries if e.get("success"))
        rate = int((success / total) * 100)

        color = ""
        if rate >= 75:
            color = "\033[92m"  # zelena
        elif rate >= 50:
            color = "\033[93m"  # žuta
        else:
            color = "\033[91m"  # crvena

        bar = "#" * int(rate / 5)
        print(f"{color}{attack_type:<10} | {bar:<20} {rate}%\033[0m")

if __name__ == "__main__":
    data = load_history()
    if data:
        display_heatmap(data)
