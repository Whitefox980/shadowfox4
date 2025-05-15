import os

def shadowops_menu():
    while True:
        print("""
        === SHADOWOPS v4 – OFFENSIVE CLI ===

        [1] Istorija skeniranja (Scan History)
        [2] Detaljan pregled misija (Mission Log)
        [3] Pregled payload-a (Payload Browser)
        [4] Praćenje fuzz modula (Fuzz Tracker)
        [5] Eksport svih PDF izveštaja (Shadow Export)

        [0] Nazad
        """)
        choice = input("Izbor: ").strip()

        if choice == "1":
            os.system("python scripts/scan_history.py")
        elif choice == "2":
            os.system("python scripts/mission_log.py")
        elif choice == "3":
            os.system("python scripts/payload_browser.py")
        elif choice == "4":
            os.system("python scripts/fuzz_tracker.py")
        elif choice == "5":
            os.system("python scripts/shadow_export.py")
        elif choice == "0":
            break
        else:
            print("[WARN] Nepoznata komanda.\n")

if __name__ == "__main__":
    shadowops_menu()
