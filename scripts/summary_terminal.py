import json
from collections import defaultdict
from rich.console import Console
from rich.table import Table

console = Console()

def summarize(path="data/fuzz_history.json"):
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except Exception as e:
        console.print(f"[red]Greška pri čitanju: {e}[/red]")
        return

    table = Table(title="ShadowFox AI Fuzzing Summary")
    table.add_column("Attack Type", style="cyan")
    table.add_column("Total", justify="right")
    table.add_column("Success", justify="right")
    table.add_column("Success Rate", justify="right")

    for attack_type, results in data.items():
        total = len(results)
        success = sum(1 for r in results if r.get("success"))
        rate = f"{(success / total * 100):.1f}%" if total > 0 else "0%"
        table.add_row(attack_type, str(total), str(success), rate)

    console.print(table)

if __name__ == "__main__":
    summarize()
