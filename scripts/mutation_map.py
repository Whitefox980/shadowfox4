import json
import os

def load_history(path="data/fuzz_history.json"):
    if not os.path.exists(path):
        print("[MAPA] Nema fuzz istorije.")
        return {}
    with open(path) as f:
        return json.load(f)

def show_mutation_map(data):
    print("\n[MAPA] Vizuelna mutacija payload-a:\n")
    for attack_type, payloads in data.items():
        print(f"\n== {attack_type.upper()} ==")
        base_seen = set()
        for entry in payloads:
            full = str(entry["payload"])
            base = full[:25]  # prva verzija mutacije
            if base in base_seen:
                continue
            base_seen.add(base)

            print(f"  [BASE] {base}...")
            for subentry in payloads:
                if str(subentry["payload"]).startswith(base):
                    mark = "✔" if subentry["success"] else "✖"
                    print(f"    {mark} {subentry['payload']}")

if __name__ == "__main__":
    data = load_history()
    if data:
        show_mutation_map(data)
