import json
from collections import defaultdict
import os

def load_history(path="data/fuzz_history.json"):
    if not os.path.exists(path):
        print("[TRACKER] Nema fuzz istorije.")
        return {}

    with open(path) as f:
        return json.load(f)

def summarize(history):
    summary = defaultdict(lambda: {"total": 0, "success": 0})

    for attack_type, attempts in history.items():
        for entry in attempts:
            summary[attack_type]["total"] += 1
            if entry.get("success"):
                summary[attack_type]["success"] += 1

    return summary

def display(summary):
    print("\n[TRACKER] AI Evolucija Fuzz Napada:\n")
    for typ, data in summary.items():
        total = data["total"]
        succ = data["success"]
        rate = (succ / total) * 100 if total > 0 else 0
        bar = "#" * int(rate / 5)
        print(f" - {typ}: {succ}/{total} uspešno ({rate:.1f}%) {bar}")

if __name__ == "__main__":
    history = load_history()
    summary = summarize(history)
    display(summary)
