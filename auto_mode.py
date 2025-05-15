# auto_mode.py

from agents.operator import run_operator
from agents.recon_agent import analyze_target
from agents.ai_brain import suggest_vectors
from agents.kljucar import generate_plan
from agents.smart_shadow_agent import SmartShadowAgent

import sys

def auto_attack(target):
    print(f"[AUTO] 1. Pokrećem Operatera za: {target}")
    run_operator(target)

    print("[AUTO] 2. AI izviđač analizira metu...")
    meta = analyze_target(target)

    print("[AUTO] 3. AI mozak predlaže vektore...")
    vectors = suggest_vectors(meta)

    print("[AUTO] 4. Ključar pravi plan napada...")
    plan = generate_plan(vectors)

    print("[AUTO] 5. SmartAgentX napada metu...")
    agent = SmartShadowAgent(meta)
    agent.run(target, plan["modules"])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auto_mode.py <target_url>")
        sys.exit(1)

    target_url = sys.argv[1]
    auto_attack(target_url)
