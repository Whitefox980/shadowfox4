import os
import json

MISSION_DIR = "data/mission_logs"

def detect_vector(payload):
    payload = payload.lower()
    if any(x in payload for x in ["<script>", "onerror", "svg", "alert"]):
        return "XSS"
    elif any(x in payload for x in ["127.0.0.1", "localhost", "169.254"]):
        return "SSRF"
    elif "etc/passwd" in payload or "boot.ini" in payload:
        return "LFI"
    elif any(x in payload for x in ["or 1=1", "drop table", '" OR "" =']):
        return "SQL Injection"
    else:
        return "unknown"

def patch_logs():
    for file in os.listdir(MISSION_DIR):
        if not file.endswith(".json"):
            continue
        path = os.path.join(MISSION_DIR, file)
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Ne mogu da učitam {file}: {e}")
            continue

        changed = False
        fixed_results = []
        for r in data.get("results", []):
            if isinstance(r, dict):
                if "signature" not in r:
                    r["signature"] = {"vector": detect_vector(r.get("payload", ""))}
                    changed = True
                fixed_results.append(r)
            elif isinstance(r, str):
                fixed_results.append({
                    "payload": r,
                    "success": True,
                    "signature": {"vector": detect_vector(r)}
                })
                changed = True

        if changed:
            data["results"] = fixed_results
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"[PATCH] Ispravljen fajl: {file}")

if __name__ == "__main__":
    patch_logs()
