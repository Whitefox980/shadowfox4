import time
import json
import os

def live_feed():
    path = "data/fuzz_history.json"
    seen = set()

    print("\n[SHADOW FEED] Pratim nove payload-e...\n(Pritisni CTRL+C za izlaz)\n")

    try:
        while True:
            if not os.path.exists(path):
                print("[ČEKAM] Nema još fajla...")
                time.sleep(2)
                continue

            with open(path) as f:
                data = json.load(f)

            for target, payloads in data.items():
                for p in payloads:
                    uid = f"{target}|{p['payload']}"
                    if uid not in seen:
                        seen.add(uid)
                        status = "✔" if p.get("success") else "✖"
                        print(f"[{target}] {status} {p['payload']}")

            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[ZATVARANJE FEED-a]\n")

if __name__ == "__main__":
    live_feed()
