import json
import os

HISTORY_PATH = "data/fuzz_history.json"

def load_fuzz():
    if not os.path.exists(HISTORY_PATH):
        print("[KLASIFIKATOR] Nema fuzz istorije.")
        return {}
    with open(HISTORY_PATH) as f:
        return json.load(f)

def classify(payload):
    if isinstance(payload, dict) and "role" in payload:
        return "JWT", "Srednja"
    p = str(payload).lower()
    if "script" in p or "alert" in p:
        return "XSS", "Srednja"
    if "' or" in p or '" or' in p:
        return "SQL Injection", "Visoka"
    if "127.0.0.1" in p or "internal" in p:
        return "SSRF", "Visoka"
    return "Nepoznata", "Niska"

def show_classified(fuzz_data):
    print("\n[KLASIFIKATOR] Detektovane ranjivosti:\n")
    for attack_type, entries in fuzz_data.items():
        for e in entries:
            if not e.get("success"):
                continue
            typ, sev = classify(e["payload"])
            print(f"[{typ:<15}] ({sev})  →  {e['payload']}")

if __name__ == "__main__":
    fuzz_data = load_fuzz()
    if fuzz_data:
        show_classified(fuzz_data)
