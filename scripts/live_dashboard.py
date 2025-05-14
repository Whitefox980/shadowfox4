import json
import os
import time
from rich.live import Live
from rich.table import Table
from rich.panel import Panel

HISTORY_PATH = "data/fuzz_history.json"

def load_history():
    if not os.path.exists(HISTORY_PATH):
        return {}
    with open(HISTORY_PATH) as f:
        return json.load(f)

def build_table(history):
    table = Table(title="ShadowFox - Live Fuzz Dashboard")
    table.add_column("Attack Type", justify="left")
    table.add_column("Success", justify="center")
    table.add_column("Total", justify="center")
    table.add_column("Rate", justify="right")

    for attack_type, entries in history.items():
        total = len(entries)
        success = sum(1 for e in entries if e.get("success"))
        rate = f"{round((success / total) * 100, 2)}%" if total else "0%"
        table.add_row(attack_type, str(success), str(total), rate)

    return table

def live_dashboard():
    with Live(refresh_per_second=1) as live:
        while True:
            history = load_history()
            table = build_table(history)
            live.update(Panel(table, title="[bold green]ShadowFox Mission Center", border_style="green"))
            time.sleep(2)

if __name__ == "__main__":
    live_dashboard()
