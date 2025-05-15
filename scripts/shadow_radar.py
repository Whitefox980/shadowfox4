import os
import json
from collections import Counter
import matplotlib.pyplot as plt

MISSION_DIR = "logs/mission_logs"

def prikupi_vektore():
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
                        vector = r.get("signature", {}).get("vector", "unknown")
                        counter[vector] += 1
        except:
            continue
    return counter

def prikazi_pie_chart(vektor_stat):
    labels = vektor_stat.keys()
    sizes = vektor_stat.values()

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Distribucija Napadnih Vektora")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    stats = prikupi_vektore()
    if not stats:
        print("[INFO] Nema detektovanih vektora.")
    else:
        for v, c in stats.most_common():
            print(f"- {v}: {c}x")
        prikazi_pie_chart(stats)
