import json
import os

def show_status():
    status_path = "data/agent_status.json"
    if not os.path.exists(status_path):
        print("[INFO] Nema status fajla. Agent još nije izvršavao misije.")
        return

    with open(status_path) as f:
        status = json.load(f)

    print("\n--- STATUS AGENATA ---")
    for agent, info in status.items():
        print(f"[{agent}]")
        print(f"  Poslednja meta : {info.get('target', 'N/A')}")
        print(f"  Aktivnost      : {info.get('activity', 'Idle')}")
        print(f"  Poslednji akcija: {info.get('last_action', 'N/A')}")
        print()

if __name__ == "__main__":
    show_status()
