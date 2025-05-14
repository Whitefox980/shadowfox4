import os
import sys
import time

MENU = """
[ SHADOWOPS - TERMINAL KOMANDA ]

1. Pokreni AI napad (SmartShadowAgent)
2. Prikaži LIVE dashboard (Fuzz rezultati)
3. Prikaži HEATMAP uspeha po tipu
4. Prikaži MAPU META (prioriteti)
5. Prikaži EVOLUCIJU PAYLOAD-a
6. Prikaži AI PREDIKCIJU sledećeg modula
7. Prikaži KLASIFIKACIJU ranjivosti
8. Generiši SHADOWBRIEF PDF izveštaj
9. Pokreni AI simulaciju payload-a
10. Prikaži SHADOWRADAR (vizuelna ranjivost)
11. Izvezi sve (ShadowExport ZIP)
12. Auto AI misija (ShadowTactics)
13. Prikaži log operacija
0. IZLAZ
"""

def run_cmd(script, path="scripts/"):
    os.system(f"PYTHONPATH=. python {path}{script}")

def main():
    while True:
        os.system("clear")
        print(MENU)
        choice = input("Izbor > ").strip()

        if choice == "1":
            target = input("Unesi metu (URL): ").strip()
            os.system(f"PYTHONPATH=. python auto_mode.py {target}")
        elif choice == "2":
            run_cmd("live_dashboard.py")
        elif choice == "3":
            run_cmd("heatmap.py")
        elif choice == "4":
            run_cmd("target_priority_map.py")
        elif choice == "5":
            run_cmd("evolve_payloads.py")
        elif choice == "6":
            run_cmd("next_attack_prediction.py")
        elif choice == "7":
            run_cmd("vuln_classifier.py")
        elif choice == "8":
            run_cmd("shadow_brief.py")
        elif choice == "9":
            run_cmd("simulate_payloads.py")
        elif choice == "10":
            run_cmd("shadow_radar.py")
        elif choice == "11":
            run_cmd("shadow_export.py")
        elif choice == "12":
            run_cmd("shadow_tactics.py")
        elif choice == "13":
            run_cmd("operator_log.py")

        elif choice == "0":
            print("Zatvaram komandni centar...")
            break
        else:
            print("Nepoznata komanda.")
        input("\n[Pritisni ENTER za povratak u meni...]")

if __name__ == "__main__":
    main()
