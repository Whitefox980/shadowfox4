import sys
import os
sys.path.insert(0, os.path.abspath("."))

from core.strateg import Strateg

def display():
    strateg = Strateg()
    stats = strateg.analyze()

    if not stats:
        print("[STRATEG] Nema rezultata.")
        return

    print("\n[STRATEG] Analiza uspeha po tipu napada:")
    for typ, data in stats.items():
        hit = data["hits"]
        total = data["total"]
        rate = round((hit / total) * 100, 2)
        bar = "#" * int(rate / 5)
        print(f" - {typ}: {hit}/{total} uspešno ({rate}%) {bar}")

if __name__ == "__main__":
    display()
