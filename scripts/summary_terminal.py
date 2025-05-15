import json
from collections import Counter
from rich.console import Console
from rich.table import Table

console = Console()

def summarize(path="data/fuzz_history.json"):
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except Exception as e:
        console.print(f"[red]Greška pri čitanju fajla: {e}[/red]")
        return

    if not data:
        console.print("[yellow]Nema dostupnih rezultata za prikaz.[/yellow]")
        return

    by_vector = Counter()
    success_by_vector = Counter()

    for entry in data:
        vector = entry.get("db_type", "Unknown")  # ili "vector" ako koristiš to
        by_vector[vector] += 1
        if entry.get("success"):
            success_by_vector[vector] += 1

    table = Table(title="ShadowFox Fuzzing Summary", show_lines=True)
    table.add_column("Vector", style="bold green")
    table.add_column("Total", justify="right")
    table.add_column("Success", justify="right")
    table.add_column("Success Rate", justify="right")

    for vector in by_vector:
        total = by_vector[vector]
        success = success_by_vector.get(vector, 0)
        rate = f"{(success / total * 100):.1f}%" if total else "0%"
        table.add_row(vector, str(total), str(success), rate)

    console.print(table)

if __name__ == "__main__":
    summarize()
