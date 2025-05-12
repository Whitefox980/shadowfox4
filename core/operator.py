import json
from agents.operater import AIOperater
from agents.kljucar import Kljucar
from agents.shadow_agent import ShadowAgent
from core.strateg import Strateg
from scripts.generate_report import generate_pdf

class ShadowOperator:
    def __init__(self, target_url):
        self.target_url = target_url
        self.targets = [target_url]
        self.paths = {
            "analysis": "data/analysis.json",
            "plan": "data/attack_plan.json",
            "results": "data/scan_results.json",
            "summary": "data/summary.json",
            "pdf": "data/report.pdf"
        }

    def save(self, data, path):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def start_mission(self):
        print(f"\n[ShadowOperator] Pokrećem misiju za metu: {self.target_url}\n")

        # 1. Operater
        print("[1] Operater analizira metu...")
        oper = AIOperater(self.target_url)
        analysis = oper.analyze()
        self.save(analysis, self.paths["analysis"])
        self.save(self.targets, "data/targets.json")

        # 2. Ključar
        print("[2] Ključar bira alate...")
        kljucar = Kljucar(analysis)
        plan = kljucar.generate_attack_plan()
        self.save(plan, self.paths["plan"])

        # 3. Shadow Agent
        print("[3] ShadowAgent kreće u akciju...")
        agent = ShadowAgent(plan, self.targets)
        results = agent.execute_plan()
        self.save(results, self.paths["results"])

        # 4. Strateg
        print("[4] Strateg analizira rezultate...")
        strateg = Strateg(self.paths["results"])
        strateg.save_summary()

        # 5. PDF izveštaj
        print("[5] Generišem PDF izveštaj...")
        generate_pdf()

        print("\n[ZAVRŠENO] Misija je uspešno kompletirana!\n")

# Primer pokretanja
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python core/operator.py <target_url>")
        sys.exit(1)
    ShadowOperator(sys.argv[1]).start_mission()
