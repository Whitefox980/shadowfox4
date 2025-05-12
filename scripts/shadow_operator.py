import json
import os
import subprocess
from datetime import datetime

def load_scan_results():
    path = "data/scan_results.json"
    if not os.path.exists(path):
        return {}

    with open(path) as f:
        return json.load(f)

def analyze_results(results):
    summary = {}
    for module, data in results.items():
        count = 0
        if isinstance(data, dict):
            for verdict in data.values():
                if "VULNERABLE" in str(verdict):
                    count += 1
        summary[module] = count
    return summary

def show_operator_dashboard():
    print("\n==== SHADOWFOX OPERATOR PANEL ====\n")
    results = load_scan_results()
    if not results:
        print("Nema dostupnih rezultata. Pokreni misiju prvo.")
    else:
        modules = list(results.keys())
        meta_example = list(results[modules[0]].keys())[0] if isinstance(results[modules[0]], dict) else "N/A"

        print(f"Meta: {meta_example}")
        print(f"Modula korišćeno: {len(modules)}")
        print("Vreme: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
        print("\n--- Detekcije po modulu ---")

        stats = analyze_results(results)
        for mod, count in stats.items():
            print(f"- {mod}: {count} ranjivosti")

        print("\nIzveštaji:")
        if os.path.exists("data/mission_log.pdf"):
            print("✓ mission_log.pdf")
        if os.path.exists("data/mission_log.md"):
            print("✓ mission_log.md")

    print("\n[1] Pokreni novu misiju (auto_mode.py)")
    print("[2] Regeneriši PDF izveštaj (export_pdf.py)")
    print("[0] Izlaz")

    izbor = input("\nUnesi opciju: ").strip()
    if izbor == "1":
        subprocess.run(["python", "auto_mode.py"])
    elif izbor == "2":
        subprocess.run(["python", "scripts/export_pdf.py"])
    else:
        print("Zatvaranje panela.")

if __name__ == "__main__":
    show_operator_dashboard()
