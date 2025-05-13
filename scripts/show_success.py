import json
import os

def show_payloads(attack_type="XSS", limit=30):
    path = "data/fuzz_history.json"

    if not os.path.exists(path):
        print("[ERROR] Nema fajla sa istorijom fuzzovanja.")
        return

    with open(path, "r") as f:
        history = json.load(f)

    payloads = history.get(attack_type, [])
    success_hits = [p["payload"] for p in payloads if p.get("success")]

    print(f"[INFO] Prikazujem poslednjih {limit} uspešnih payload-a za: {attack_type}")
    for i, payload in enumerate(success_hits[-limit:], 1):
        print(f"{i}. {payload}")

if __name__ == "__main__":
    show_payloads("XSS")  # ili promeni u "SQLi", "SSRF" itd.
