import random
from core.mutation_engine import MutationEngine

def simulate():
    engine = MutationEngine()
    attack_types = ["SQLi", "XSS", "JWT", "SSRF"]
    print("\n[SIMULATOR] AI predikcija uspešnosti payload-a:\n")
    for atype in attack_types:
        base = engine.generate_payload(atype)
        mutations = engine.mutate_payload(base)
        print(f"\n== {atype.upper()} ({len(mutations)} mutacija) ==")
        for m in mutations:
            prediction = random.choice(["Uspešan", "Neuspešan"])
            print(f" - {m}  →  {prediction}")

if __name__ == "__main__":
    simulate()
