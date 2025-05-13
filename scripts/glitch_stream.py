from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from time import sleep
import random
import json

def load_payloads(path="data/attack_stats.json"):
    try:
        with open(path, "r") as f:
            data = json.load(f)
            all_payloads = []
            for target, entries in data.items():
                for payload, result in entries.items():
                    all_payloads.append((target, payload, result))
            return all_payloads
    except:
        return []

def render_table(data, limit=25):
    table = Table(title="[bold green]Live Payload Feed", expand=True)
    table.add_column("Target")
    table.add_column("Payload")
    table.add_column("Status")

    for row in data[-limit:]:
        target, payload, result = row
        color = "green" if result == "Success" else "red"
        table.add_row(target, payload, f"[bold {color}]{result}[/]")

    return table

def run_stream():
    payloads = load_payloads()
    stream = []

    with Live(Panel(render_table(stream)), refresh_per_second=10) as live:
        while True:
            payloads = load_payloads()
            if payloads:
                stream.append(random.choice(payloads))
                stream = stream[-100:]  # keep recent
                live.update(Panel(render_table(stream)))
            sleep(0.3)

if __name__ == "__main__":
    run_stream()
