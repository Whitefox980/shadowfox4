import json
import os
from collections import defaultdict

HISTORY_PATH = "data/mission_history.json"

def load_missions():
    if not os.path.exists(HISTORY_PATH):
        print("[MAPA META] Nema istorije misija.")
        return []
    with open(HISTORY_PATH) as f:
        return json.load(f)

def calculate_priorities(missions):
    score_map = defaultdict(lambda: {"success": 0, "total": 0})

    for mission in missions:
        target = mission.get("target")
        results = mission.get("results", {})
        for payload, success in results.items():
            score_map[target]["total"] += 1
            if success:
                score_map[target]["success"] += 1

    priority_list = []
    for target, score in score_map.items():
        success = score["success"]
        total = score["total"]
        rate = (success / total) * 100 if total else 0
        priority_list.append((target, success, total, round(rate, 2)))

    return sorted(priority_list, key=lambda x: x[3], reverse=True)

def show_priority_map():
    missions = load_missions()
    priorities = calculate_priorities(missions)

    print("\n[MAPA META] Prioriteti za sledeće misije:\n")
    for i, (target, s, t, rate) in enumerate(priorities, 1):
        bar = "#" * int(rate / 5)
        print(f"{i}. {target:<40} {s}/{t} uspešno ({rate}%) {bar}")

if __name__ == "__main__":
    show_priority_map()
