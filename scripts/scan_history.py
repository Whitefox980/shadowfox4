import json
import os

def show_history():
    path = "data/mission_history.json"

    if not os.path.exists(path):
        print("[!] Nema istorije skeniranja.")
        return

    with open(path) as f:
        data = json.load(f)

    if not data:
        print("[!] Fajl postoji, ali nema zapisa.")
        return

    print("\n[SHADOW SCAN HISTORY]\n")
    for i, mission in enumerate(reversed(data[-20:]), 1):
        target = mission.get("target", "Nepoznata")
        timestamp = mission.get("timestamp", "Nepoznat")
        results = mission.get("results", {})
        modules = ", ".join(results.keys()) if isinstance(results, dict) else "Nepoznato"
        print(f"{i:>2}. {timestamp} | {target} | Moduli: {modules}")

if __name__ == "__main__":
    show_history()
