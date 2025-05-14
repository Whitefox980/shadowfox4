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
from core.smart_shadow_agent import SmartShadowAgent
from core.strateg import Strateg

def save_results(results, target):
    from datetime import datetime

    # 1. Summary zapis
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    summary = {
        "time": timestamp,
        "target": target,
        "modules": list(results),
        "hits": sum("VULNERABLE" in str(r) for r in results.values())
    }

    try:
        with open("data/mission_history.json", "r") as f:
            history = json.load(f)
            if not isinstance(history, list):
                print("[WARN] mission_history.json nije lista — resetujem.")
                history = []
    except:
        history = []

    history.append(summary)

    with open("data/mission_history.json", "w") as f:
        json.dump(history, f, indent=2)

    # 2. Payload zapis
    try:
        with open("data/payload_results.json", "r") as f:
            rawlog = json.load(f)
            if not isinstance(rawlog, dict):
                print("[WARN] payload_results.json nije dict — resetujem.")
                rawlog = {}
    except:
        rawlog = {}

    rawlog[target] = results  # poslednji rezultat po meti

    with open("data/payload_results.json", "w") as f:
        json.dump(rawlog, f, indent=2)

    print("[AUTO] Rezultati sačuvani u oba fajla.")
def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_mode.py <target_url> [--dashboard]")
        return

    target_url = sys.argv[1]
    use_dashboard = "--dashboard" in sys.argv

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

    # 3. Kljucar bira alate
    print("[AUTO] 3. Kljucar bira alate...")
    kljucar = Kljucar(site_data)
    modules_selected = kljucar.generate_plan(plan)

    # 4. ShadowAgent izvršava napade
    print("[AUTO] 4. ShadowAgent izvršava napade...")
    agent = ShadowAgent(modules_selected, target=target_url)
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

    # 8. Pokreni dashboard ako je traženo
    if use_dashboard:
        subprocess.Popen(["python", "scripts/live_dashboard.py"], start_new_session=True)
        print("[AUTO] Pokrenut dashboard u pozadini.")
    from scripts.export_to_pdf import export_to_pdf

# Posle save_results(...)
    export_to_pdf(results, target_url)
    gc.collect()
    sys.exit(0)

if __name__ == "__main__":
    main()
