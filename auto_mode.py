import sys
import json
import subprocess
import gc
from datetime import datetime

from scripts.export_pdf import export_to_pdf
from agents.operator import Operater
from core.ai_brain import BrainSuggestion
from agents.kljucar import Kljucar
from agents.shadow_agent import ShadowAgent
from agents.smart_shadow_agent import SmartShadowAgent
from core.strateg import Strateg

def save_results(results, target):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    summary = {
        "time": timestamp,
        "target": target,
        "modules": list(results),
        "vulns": sum("VULNERABLE" in str(r) for r in results.values())
    }
    try:
        with open("data/mission_history.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    history.append(summary)

    with open("data/mission_history.json", "w") as f:
        json.dump(history, f, indent=2)

def main():
    if len(sys.argv) != 2:
        print("Usage: python auto_mode.py <target_url>")
        return

    target_url = sys.argv[1]

    # 1. Operater analizira metu
    print(f"\n[AUTO] 1. Pokrećem Operatera za: {target_url}")
    operator = Operater(target_url)
    analysis = operator.analyze()
    site_data = analysis["site_data"]

    # 2. AI bira module
    print("[AUTO] 2. AI odlučuje koje module koristiti...")
    brain = BrainSuggestion(site_data)
    plan = brain.plan()
    print("[AI BRAIN] Preporučeni moduli:", plan)

    # 3. Ključar bira alate
    print("[AUTO] 3. AI Ključar bira alate...")
    kljucar = Kljucar(site_data)
    selected = kljucar.generate_plan()

    # 4. ShadowAgent izvršava napade
    print("[AUTO] 4. ShadowAgent izvršava napade...")
    agent = ShadowAgent(modules=selected, target=target)
    results = agent.execute_plan()
    print(f"[SMART] Završeno skeniranje sa {sum(1 for v in results.values() if isinstance(v, list) or v)} payload-a.")

    # 5. Strateg pamti i unapređuje AI
    print("[AUTO] 5. Strateg pamti rezultate i unapređuje AI...")
    s = Strateg()
    s.scan = results
    s.generate_strategy(results)

    # 6. SmartShadowAgent za napredno učenje
    smart_agent = SmartShadowAgent()
    smart_agent.target = target_url
    smart_agent.run()

    # 7. Sačuvaj rezultate
    save_results(results, target_url)

    # 8. Pokreni dashboard
    subprocess.Popen(["python", "scripts/live_dashboard.py"], start_new_session=True)
    print("[AUTO] Pokrenut dashboard u pozadini.")

    gc.collect()
    sys.exit(0)

if __name__ == "__main__":
    main()
