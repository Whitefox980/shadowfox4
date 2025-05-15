import os
import json
from collections import Counter

MISSION_DIR = "data/mission_logs"

RECOMMENDATIONS = {
    "XSS": "Koristi Content-Security-Policy (CSP) header i proper HTML escaping.",
    "SQL Injection": "Koristi parametrizovane upite (prepared statements).",
    "LFI": "Validiraj i filtriraj sve korisničke fajl putanje.",
    "SSRF": "Zabrani pristup internim IP-ima i koristi allow-list za URL-ove.",
    "BruteForce": "Ograniči broj pokušaja i koristi CAPTCHA sisteme.",
    "unknown": "Dodaj dodatnu AI analizu za nedefinisane vektore."
}

def load_vectors():
    counter = Counter()
    for file in os.listdir(MISSION_DIR):
        if not file.endswith(".json"):
            continue
        path = os.path.join(MISSION_DIR, file)
        try:
            with open(path, "r") as f:
                data = json.load(f)
            for r in data.get("results", []):
                if isinstance(r, dict):
                    vec = r.get("signature", {}).get("vector", "unknown")
                    counter[vec] += 1
        except Exception as e:
            print(f"[ERROR] Ne mogu da obradim {file}: {e}")
    return counter

def generate_advice():
    vectors = load_vectors()
    print("\n=== WHITE SHADOW ADVISOR ===\n")
    print("Analiza detektovanih vektora napada i preporuke:\n")

    for vec, count in vectors.most_common():
        advice = RECOMMENDATIONS.get(vec, "Nema konkretne preporuke za ovaj tip.")
        print(f"- {vec} ({count}x): {advice}")

    print("\n[INFO] Pregled završeno.")

if __name__ == "__main__":
    generate_advice()
