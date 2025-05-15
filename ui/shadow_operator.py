import os
import json
from datetime import datetime

LOG_DIR = "data/mission_logs"

def load_missions():
    missions = []
    for file in os.listdir(LOG_DIR):
        if file.endswith(".json"):
            path = os.path.join(LOG_DIR, file)
            try:
                with open(path, "r") as f:
                    data = json.load(f)

                # Ekstrakcija vektora
                vectors = []
                for r in data.get("results", []):
                    if isinstance(r, dict):
                        vec = r.get("signature", {}).get("vector")
                        if vec:
                            vectors.append(vec)

                missions.append({
                    "file": file,
                    "target": data.get("target", "Nepoznata"),
                    "timestamp": data.get("timestamp", "N/A"),
                    "payload_count": len(data.get("results", [])),
                    "vectors": list(set(vectors)) if vectors else ["unknown"]
                })
            except Exception as e:
                print(f"[ERROR] Ne mogu da obradim {file}: {e}")
    return sorted(missions, key=lambda x: x["timestamp"], reverse=True)

def show_summary():
    missions = load_missions()
    print("\n=== SHADOW OPERATOR: Pregled Misija ===\n")
    for i, m in enumerate(missions[:10]):
        vreme = m["timestamp"]
        meta = m["target"]
        broj = m["payload_count"]
        vektori = ", ".join(m["vectors"]) if m["vectors"] else "N/A"
        print(f"{i+1}. {vreme} | {meta} | Payload-a: {broj} | Vektori: {vektori}")
    print("\nUkupno misija:", len(missions))

if __name__ == "__main__":
    show_summary()
