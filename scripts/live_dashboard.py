import json
import os
from datetime import datetime

def show_dashboard():
    print("\n=== SHADOWFOX LIVE DASHBOARD ===\n")

    # Agent Status
    status_path = "data/agent_status.json"
    if os.path.exists(status_path):
        with open(status_path) as f:
            agents = json.load(f)

        print(">> AGENT STATUS:")
        for agent, info in agents.items():
            print(f"  - {agent}: {info.get('activity')} on {info.get('target')} @ {info.get('updated_at')}")
    else:
        print("  [!] Nema podataka o agentima.")

    # Mission History
    hist_path = "data/mission_history.json"
    if os.path.exists(hist_path):
        with open(hist_path) as f:
            history = json.load(f)

        print("\n>> POSLEDNJE MISIJE:")
        for entry in history[-5:]:  # Poslednjih 5
            print(f"  - {entry['timestamp']} | {entry['target']} | {entry['vulns']} ranjivosti | {len(entry['modules'])} modula")
    else:
        print("\n  [!] Nema istorije misija.")

if __name__ == "__main__":
    show_dashboard()
