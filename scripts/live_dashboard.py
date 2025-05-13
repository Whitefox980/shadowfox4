import json
import time
from rich.table import Table
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from rich import box

def show_dashboard(stats, limit=30):
    console = Console()
    console.clear()

    for target, results in stats.items():
        # Samo poslednjih N rezultata za lagani prikaz
        latest = results[-limit:] if isinstance(results, list) else results
        if not latest:
            continue

        console.rule(f"[bold green]Rezultati za metu: {target}")

        # Brz prebroj uspešnih/neudatih
        success_count = sum(1 for r in latest.values() if r == "Success")
        total_count = len(latest)
        fail_count = total_count - success_count

        # Status Bar
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None),
            TextColumn("[green]{task.completed} uspešno [red]{task.fields[fail]} neuspešno"),
            transient=True,
        ) as progress:
            task = progress.add_task("[cyan]Napad AI agenta...", total=total_count, fail=fail_count)
            progress.update(task, completed=success_count)

        # Tabela
        table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)
        table.add_column("Payload", width=40)
        table.add_column("Rezultat", justify="center")

        for i, (payload, result) in enumerate(latest.items()):
            if i >= limit:
                break
            color = "[green]Success" if result == "Success" else "[red]Fail"
            table.add_row(payload[:40], color)

        console.print(table)
        console.print(Panel(f"Ukupno: {total_count}  |  [green]Uspešni: {success_count}[/]  |  [red]Neuspešni: {fail_count}[/]"))
        time.sleep(0.3)  # Throttle po meti

if __name__ == "__main__":
    try:
        with open("data/attack_stats.json", "r") as f:
            stats = json.load(f)
            show_dashboard(stats, limit=30)  # Prikaz max 30 payload-a po meti
    except FileNotFoundError:
        print("[ERROR] Nema fajla sa istorijom fuzzovanja.")
