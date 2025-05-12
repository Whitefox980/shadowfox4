import json

def load_history(path="data/mission_history.json"):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print("[ERROR] Nema istorije.")
        return []

def summarize(history):
    total = len(history)
    if total == 0:
        print("Nema misija.")
        return

    max_vulns = max(history, key=lambda x: x['vulns'])
    min_vulns = min(history, key=lambda x: x['vulns'])

    print(f"\nUkupno misija: {total}")
    print(f"Meta sa najviše ranjivosti: {max_vulns['target']} ({max_vulns['vulns']})")
    print(f"Meta sa najmanje ranjivosti: {min_vulns['target']} ({min_vulns['vulns']})")

    avg = sum(m['vulns'] for m in history) / total
    print(f"Prosečan broj ranjivosti: {avg:.2f}")

if __name__ == "__main__":
    history = load_history()
    summarize(history)
