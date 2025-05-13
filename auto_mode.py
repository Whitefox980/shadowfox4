import os, sys, json, threading
from datetime import datetime
from scripts.export_pdf import export_to_pdf
# Agenti
from agents.operater import AIOperater
from agents.ai_kljucar import AIKljucar
from agents.shadow_agent import ShadowAgent

# Core
from shadow_scan_core import ShadowScanCore
from core.live_monitor import LiveMonitor
from core.strateg import Strateg
from core.ai_brain import BrainSuggestion
from core.ai_module_filter import AIModuleFilter

# 1. Učitavanje meta iz fajla
def load_targets():
    with open("data/targets.txt") as f:
        return [line.strip() for line in f if line.strip()]

# 2. Snimanje rezultata + timestamp + istorija
def save_results(results, target):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    os.makedirs("data/missions", exist_ok=True)

    with open("data/scan_results.json", "w") as f:
        json.dump(results, f, indent=2)

    with open(f"data/missions/mission_{timestamp}.json", "w") as f:
        json.dump(results, f, indent=2)

    summary = {
        "timestamp": timestamp,
        "target": target,
        "modules": len(results),
        "vulns": sum("VULNERABLE" in str(v) for r in results.values() for v in (r.values() if isinstance(r, dict) else [r]))
    }

    history_path = "data/mission_history.json"
    if os.path.exists(history_path):
        with open(history_path) as f:
            history = json.load(f)
    else:
        history = []

    history.append(summary)

    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

# 3. Glavno izvršavanje
def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_mode.py <target_url>")
        return

    url = sys.argv[1]

    print(f"\n[AUTO] 1. Pokrećem Operatera za: {url}")
    operater = AIOperater(url)
    analysis = operater.analyze()

    if not analysis or "site_data" not in analysis:
        print("[AUTO] Greška: Operater nije uspeo da analizira metu.")
        return

    print("[AUTO] 2. AI odlučuje koje module koristiti...")
    ai_suggestion = BrainSuggestion(analysis["site_data"])
    plan = ai_suggestion.plan()
    print("[AI BRAIN] Preporučeni moduli:", plan)

    scanner = ShadowScanCore([url])
    mod_filter = AIModuleFilter(scanner.modules, plan)
    selected_modules = mod_filter.extract_suggested()

    print("[AUTO] 3. AI Ključar bira alate...")
    kljucar = AIKljucar(analysis["site_data"])
    selected_tools = kljucar.decide_tools()

    print("[AUTO] 4. ShadowAgent izvršava napade...")
    agent = ShadowAgent(selected_modules, url)
    results = agent.execute_plan()

    print("[AUTO] 5. Strateg pamti rezultate i unapređuje AI...")
    s = Strateg()
    s.generate_strategy(results)

    save_results(results, url)
    print("\n[AUTO] Misija završena.")
    # === AUTO PDF EXPORT ===
try:
    with open("data/mission_history.json") as f:
        history = json.load(f)
        export_to_pdf(len(history))  # poslednja misija
except Exception as e:
    print(f"[PDF] Neuspelo automatsko kreiranje PDF: {e}")
if __name__ == "__main__":
    main()
