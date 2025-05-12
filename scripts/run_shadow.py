from agents.shadow_agent import ShadowAgent
import json

# Učitavamo attack_plan koji je prethodno sačuvan od Ključara
with open("data/attack_plan.json") as f:
    attack_plan = json.load(f)

with open("data/targets.json") as f:
    targets = json.load(f)

agent = ShadowAgent(attack_plan, targets)
results = agent.execute_plan()

with open("data/scan_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("[SHADOW_AGENT] Testiranje završeno. Rezultati sačuvani.")
