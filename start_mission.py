import sys
import json
import os

from agents.operater import AIOperater
from agents.kljucar import Kljucar
from agents.shadow_agent import ShadowAgent
from core.strateg import Strateg
from scripts.view_report import show_summary, load_summary

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def run_all(target_url):
    print(f"\n[+] META: {target_url}\n")

    # Operater
    print("[1] Analiza mete (Operater)...")
    oper = AIOperater(target_url)
    analysis = oper.analyze()
    save_json(analysis, "data/analysis.json")
    save_json([target_url], "data/targets.json")

    # Kljucar
    print("[2] Generišem plan napada (Kljucar)...")
    kljucar = Kljucar(analysis)
    plan = kljucar.generate_attack_plan()
    save_json(plan, "data/attack_plan.json")

    # ShadowAgent
    print("[3] Shadow agent kreće u napad...")
    agent = ShadowAgent(plan, [target_url])
    results = agent.execute_plan()
    save_json(results, "data/scan_results.json")

    # Strateg
    print("[4] Generišem rezime (Strateg)...")
    strategist = Strateg("data/scan_results.json")
    strategist.save_summary()

    # Pregled
    print("[5] Prikaz rezultata...\n")
    summary = load_summary()
    show_summary(summary)

    # PDF
    print("[6] Kreiram PDF izveštaj...")
    from scripts.generate_report import generate_pdf
    generate_pdf()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python start_mission.py <URL>")
        sys.exit(1)
    run_all(sys.argv[1])
