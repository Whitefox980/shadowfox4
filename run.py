import sys
import os

def run_module(name, args=""):
    print(f"\n\033[92m[SHADOWFOX] Pokrećem modul: {name}\033[0m")
    os.system(f"python {name} {args}")

def main():
    while True:
        os.system("clear")
        print("""
\033[92m
███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗███████╗██╗  ██╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║██╔════╝╚██╗██╔╝
█████╗  ███████║███████║██║  ██║██║   ██║██║ █╗ ██║█████╗   ╚███╔╝ 
██╔══╝  ██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║██╔══╝   ██╔██╗ 
███████╗██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝███████╗██╔╝ ██╗
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝
                   SHADOWFOX v4 - COMMAND CENTER
\033[0m
\033[92m══════════════════════════════════════════════════════════════════\033[0m
 [1]  Automatska Misija            [7]  ShadowRadar (statistike)
 [2]  Shadow Operator              [8]  ShadowTactician (strateg)
 [3]  WhiteShadowAdvisor           [9]  ShadowOps CLI (eksploatacija)
 [4]  Eksportuj PDF savet          [10] ShadowExploitBuilder
 [5]  Eksportuj PDF izveštaj       [11] SHADOWOPS TERMINAL
 [6]  Zakrpi stare logove
\033[92m══════════════════════════════════════════════════════════════════\033[0m
 [0]  Izlaz
""")

        choice = input("\033[96m[Izbor] > \033[0m").strip()

        if choice == "1":
            target = input("\033[96m[Meta URL] > \033[0m").strip()
            run_module("auto/auto_mode.py", target)
        elif choice == "2":
            run_module("ui/shadow_operator.py")
        elif choice == "3":
            run_module("white_shadow_advisor.py")
        elif choice == "4":
            run_module("reports/advisor_export.py")
        elif choice == "5":
            run_module("reports/report_export.py")
        elif choice == "6":
            run_module("auto/patch_logs.py")
        elif choice == "7":
            run_module("scripts/shadow_radar.py")
        elif choice == "8":
            run_module("scripts/shadow_tactics.py")
        elif choice == "9":
            run_module("scripts/shadowops_cli.py")
        elif choice == "10":
            run_module("scripts/shadow_export.py")
        elif choice == "11":
            run_module("shadowops.py")
        elif choice == "0":
            print("\033[91m[INFO] Zatvaram komandni centar...\033[0m")
            sys.exit()
        else:
            print("\033[91m[WARN] Nepoznata komanda.\033[0m\n")
            input("\033[90m[Pritisni ENTER za povratak u meni...]\033[0m")

if __name__ == "__main__":
    main()
