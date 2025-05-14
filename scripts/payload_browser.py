import json
import os
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt

def browse_payloads():
    path = "data/fuzz_history.json"
    if not os.path.exists(path):
        print("[red][!] Nema fajla fuzz_history.json[/red]")
        return

    with open(path) as f:
        data = json.load(f)

    vector = Prompt.ask("[blue]Filter po attack vectoru (npr. SQLi, XSS, SSRF ili ALL)[/blue]", default="ALL")
    uspeh = Prompt.ask("[green]Filter po uspešnosti (yes, no, all)[/green]", choices=["yes", "no", "all"], default="all")

    filtered = []
    for d in data:
        sig = d.get("signature", {})
        if not sig:
            continue
        if vector.upper() != "ALL" and sig.get("vector", "").upper() != vector.upper():
            continue
        if uspeh == "yes" and not d.get("success"):
            continue
        if uspeh == "no" and d.get("success"):
            continue
        filtered.append(d)

    if not filtered:
        print("[yellow]Nema rezultata za traženi filter.[/yellow]")
        return

    table = Table(title="ShadowFox Payload Arsenal")
    table.add_column("Payload", style="cyan")
    table.add_column("Vector", style="magenta")
    table.add_column("Success", justify="center", style="green")
    table.add_column("Hash", style="yellow")

    for d in filtered[:30]:  # samo prvih 30
        table.add_row(
            d["payload"][:30] + ("..." if len(d["payload"]) > 30 else ""),
            d["signature"].get("vector", "N/A"),
            "✓" if d.get("success") else "✗",
            d["signature"].get("hash", "???")[:10]
        )

    console = Console()
    console.print(table)

if __name__ == "__main__":
    browse_payloads()
