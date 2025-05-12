import json

def load_history(path="data/mission_history.json"):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print("[ERROR] Nema istorije misija.")
        return []

def list_missions(history):
    for i, entry in enumerate(history):
        print(f"[{i}] {entry['timestamp']} - Target: {entry['target']} - Vulns: {entry['vulns']}")

def show_details(history, index):
    try:
        entry = history[index]
        print("\n--- Detalji Misije ---")
        print(f"Vreme:   {entry['timestamp']}")
        print(f"Meta:    {entry['target']}")
        print(f"Ranji.:  {entry['vulns']}")
        print(f"Modula:  {entry['modules']}")
    except IndexError:
        print("[ERROR] Nevalidan ID.")

if __name__ == "__main__":
    history = load_history()
    if not history:
        exit()
    list_missions(history)
    try:
        izbor = int(input("\nUnesi broj misije za prikaz detalja: "))
        show_details(history, izbor)
    except ValueError:
        print("[ERROR] Nije unet validan broj.")
