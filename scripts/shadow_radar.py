import json, os
from collections import Counter
from matplotlib import pyplot as plt
from scripts.vuln_classifier import classify

def radar():
    with open("data/fuzz_history.json") as f:
        data = json.load(f)

    counts = Counter()
    for entries in data.values():
        for e in entries:
            if e.get("success"):
                t, _ = classify(e["payload"])
                counts[t] += 1

    labels, sizes = zip(*counts.items())
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.axis("equal")
    plt.title("ShadowRadar: Uspešne Ranjivosti")
    plt.show()

if __name__ == "__main__":
    radar()
