import json
import os
from collections import defaultdict
from rich import print
from rich.table import Table

def generate_stats():
    path = "data/fuzz_history.json"
    if not os.path.exists(path):
        print("[red][!] Nema fuzz_history.json fajla.[/red]")
        return

    with open(path) as f:
        data = json.load(f)

    stats = defaultdict(int)
    for entry in data:
        sig = entry.get("signature", {})
        if entry.get("success") and isinstance(sig, dict):
            vector = sig.get("vector", "Unknown")
            stats[vector] += 1

    if not stats:
        print("[yellow]Nema uspešnih payload-a sa potpisom.[/yellow]")
        return

    table = Table(title="ShadowFox Success Stats")
    table.add_column("Attack Vector", style="cyan", no_wrap=True)
    table.add_column("Success Count", justify="right", style="green")

    for vector, count in sorted(stats.items(), key=lambda x: -x[1]):
        table.add_row(vector, str(count))

    print(table)

if __name__ == "__main__":
    generate_stats()
