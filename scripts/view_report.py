import json
import os
from datetime import datetime

def load_summary():
    path = "data/mission_history.json"
    if not os.path.exists(path):
        return []

    with open(path) as f:
        return json.load(f)

def print_report(summary):
    if not summary:
        print("[INFO] Nema zabeleženih misija.")
        return

    print("\n=== MISIJE ===\n")
    for idx, entry in enumerate(summary[::-1], 1):
        print(f"[{idx}] {entry['timestamp']} | {entry['target']} | Modules: {entry['modules']} | Vulns: {entry['vulns']}")

    print("\nKoristi: `python scripts/view_report.py <broj>` da vidiš detalje.\n")

def load_detailed_report(index):
    summary = load_summary()
    try:
        entry = summary[::-1][index - 1]
        timestamp = entry['timestamp'].replace(":", "-")
        file_path = f"data/missions/mission_{timestamp}.json"
        with open(file_path) as f:
            data = json.load(f)
        print(f"\n=== DETALJNI IZVEŠTAJ: {entry['target']} ({entry['timestamp']}) ===\n")
        for mod, res in data.items():
            print(f"[{mod}] => {res}")
    except Exception as e:
        print(f"[ERROR] Ne mogu da učitam detalje: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
        load_detailed_report(int(sys.argv[1]))
    else:
        summary = load_summary()
        print_report(summary)
