import os
from scripts.next_attack_prediction import predict, load_history
from core.smart_shadow_agent import SmartShadowAgent

def pick_target():
    with open("data/mission_history.json") as f:
        missions = json.load(f)
    targets = [m["target"] for m in missions]
    return targets[-1] if targets else input("Unesi metu: ")

def run():
    print("[TACTICS] AI bira sledeću misiju...")
    attack_type, _ = predict(load_history())
    target = pick_target()

    print(f"[TACTICS] Meta: {target}")
    print(f"[TACTICS] Fokus: {attack_type}")
    agent = SmartShadowAgent()
    agent.run(target)

if __name__ == "__main__":
    run()
