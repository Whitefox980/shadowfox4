from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich import box
import os
import json
import subprocess
from datetime import datetime

console = Console()

def load_results():
    path = "data/scan_results.json"
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)

def analyze(results):
    summary = {}
    for mod, res in results.items():
        if isinstance(res, dict):
            count = sum(1 for v in res.values() if "VULNERABLE" in str(v))
            summary[mod] = count
        else:
            summary[mod] = 0
    return summary

def show_history():
    path = "data/mission_history.json"
    if not os.path.exists(path):
        console.print("[red]Nema snimljenih misija.")
        return

    with open(path) as f:
        history = json.load(f)

    table = Table(title="Istorija ShadowFox Misija", box=box.ROUNDED)
    table.add_column("Vreme")
    table.add_column("Meta")
    table.add_column("Modula")
    table.add_column("Detekcija")

    for item in reversed(history[-10:]):  # Poslednjih 10
        table.add_row(item["timestamp"], item["target"], str(item["modules"]), str(item["vulns"]))

    console.print(table)

def show_dashboard():
    while True:
        console.clear()
        console.rule("[bold green]ShadowFox Operator Panel")
        results = load_results()

        if not results:
            console.print("[red]Nema rezultata. Pokreni auto_mode.py prvo.")
        else:
            meta = list(results[list(results.keys())[0]].keys())[0] if isinstance(list(results.values())[0], dict) else "N/A"
            console.print(Panel.fit(
                f"[cyan]Meta:[/] {meta}\n[cyan]Vreme:[/] {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                title="Info"
            ))

            table = Table(title="Otkrivene Ranjivosti", box=box.SQUARE)
            table.add_column("Modul", style="bold yellow")
            table.add_column("Broj Ranjivosti", style="bold red")
            for mod, cnt in analyze(results).items():
                table.add_row(mod, str(cnt))
            console.print(table)

        console.print("\n[1] Pokreni auto_mode.py")
        console.print("[2] Generiši PDF izveštaj")
        console.print("[3] Prikaži istoriju misija")
        console.print("[0] Izlaz")

        izbor = Prompt.ask("\nUnesi opciju", choices=["0", "1", "2", "3"])
        if izbor == "1":
            subprocess.run(["python", "auto_mode.py"])
        elif izbor == "2":
            subprocess.run(["python", "scripts/export_pdf.py"])
        elif izbor == "3":
            show_history()
            Prompt.ask("\nPritisni Enter za povratak...")
        elif izbor == "0":
            console.print("[bold green]Zatvaranje ShadowFox Operator panela.")
            break

if __name__ == "__main__":
    show_dashboard()
