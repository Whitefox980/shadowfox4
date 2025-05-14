import sys
import os
sys.path.insert(0, os.path.abspath("."))

from core.strateg import Strateg

def suggest():
    s = Strateg()
    top_modules = s.get_priority_modules(min_success_rate=30)

    if not top_modules:
        print("[STRATEG] Nema modula koji prelaze prag uspeha.")
    else:
        print("\n[STRATEG] Predloženi moduli za sledeću misiju:")
        for m in top_modules:
            print(f" - {m}")

if __name__ == "__main__":
    suggest()
