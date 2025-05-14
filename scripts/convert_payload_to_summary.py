import json
from datetime import datetime

with open("data/payload_results.json", "r") as f:
    old_data = json.load(f)

summary = []

for target, payloads in old_data.items():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    hit_count = sum(1 for p in payloads if p.get("success"))
    summary.append({
        "time": timestamp,
        "target": target,
        "modules": ["Unknown"],  # Možeš ovde ručno menjati ako znaš
        "hits": hit_count
    })

with open("data/mission_history.json", "w") as f:
    json.dump(summary, f, indent=2)

print("[KONVERZIJA] Uspešno konvertovano u mission_history.json")
