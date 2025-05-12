from agents.kljucar import Kljucar
import json
import os

plan = Kljucar().generate_plan()

os.makedirs("data/results", exist_ok=True)
with open("data/results/kljucar_plan.json", "w") as f:
    json.dump(plan, f, indent=2)

print("\n[Ključar] Plan napada uspešno kreiran i sačuvan.")
