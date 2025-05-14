import os
import requests
import json

MENU = """
[ SHADOWOPS CLI KOMANDA ]

1. Pokreni AI napad na metu
2. Pokreni full misiju (napad + PDF)
3. Generiši samo PDF izveštaj
4. Prikaži STATUS poslednje misije
5. Prikaži poslednjih 10 logova (AI Agent operacije)
6. Prikaži najnovije payload-e
7. Eksportuj sve u ZIP ShadowFox_Export.zip
8. Pokreni SHADOW FEED (real-time prikaz payload-a)
9. Prikaži SCAN HISTORY (istorija napada)
10. Generiši HackerOne izveštaj (PDF za bug bounty)
11. Kreiraj HackerOne ZIP paket za slanje
12. Verifikuj Shadow potpis (poslednjih 10)
13. Statistika uspešnih vektora (ShadowRadar)
14. Replay uspešnog payload-a
15. Pregledaj Arsenal Payload-a (Filter + Hash)
0. Izlaz
"""

BASE_URL = "http://localhost:8000"

def ask_target():
    return input("Unesi metu (npr. https://example.com): ").strip()

def send_post(endpoint, data=None):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=data or {})
        print("\n[ODGOVOR API-ja]")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"[GREŠKA] Neuspešan zahtev: {str(e)}")

def get_status():
    try:
        response = requests.get(f"{BASE_URL}/webhook/status")
        print("\n[STATUS]")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"[GREŠKA] Neuspešan zahtev: {str(e)}")

def main():
    while True:
        os.system("clear")
        print(MENU)
        izbor = input("Izbor > ").strip()

        if izbor == "1":
            target = ask_target()
            send_post("/webhook/attack", {"target": target})
        elif izbor == "2":
            target = ask_target()
            send_post("/webhook/full-mission", {"target": target})
        elif izbor == "3":
            send_post("/webhook/report")
        elif izbor == "4":
            get_status()
        elif izbor == "5":
            try:
                with open("data/operator_log.txt") as f:
                    lines = f.readlines()[-10:]
                    print("\n[OPERATOR LOG - POSLEDNJIH 10 LINIJA]\n")
                    for line in lines:
                        print(f" - {line.strip()}")
            except:
                print("[GREŠKA] Log ne postoji.")
        elif izbor == "6":
            try:
                with open("data/fuzz_history.json") as f:
                    data = json.load(f)
                last_target = list(data.keys())[-1]
                payloads = data[last_target][-10:]  # zadnjih 10
                print(f"\n[PAYLOADI ZA {last_target}]\n")
                for p in payloads:
                    status = "✔" if p["success"] else "✖"
                    print(f"{status} {p['payload']}")
            except:
                print("[GREŠKA] Nema payload podataka.")
        elif izbor == "7":
            os.system("python scripts/shadow_export.py")

        elif izbor == "8":
            os.system("python scripts/live_feed.py")
        elif izbor == "9":
            os.system("python scripts/scan_history.py")
        elif izbor == "10":
            os.system("python scripts/h1_report.py")
        elif izbor == "11":
            os.system("python scripts/h1_package.py")

        elif izbor == "12":
            os.system("python scripts/verify_signature.py")
        elif izbor == "13":
            os.system("python scripts/module_stats.py")
        elif izbor == "14":
            os.system("python scripts/replay_payloads.py")
        elif izbor == "15":
            os.system("python scripts/payload_browser.py")


        elif izbor == "0":
            print("Izlaz iz ShadowOps CLI.")
            break
        else:
            print("Nepoznata opcija.")
        input("\nPritisni ENTER za povratak u meni...")

if __name__ == "__main__":
    main()
