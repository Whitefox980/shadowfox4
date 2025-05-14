import json
import requests
import os
from rich import print
from rich.prompt import Prompt

def replay():
    path = "data/fuzz_history.json"
    if not os.path.exists(path):
        print("[red][!] Nema fajla fuzz_history.json[/red]")
        return

    with open(path) as f:
        data = json.load(f)

    successful = [d for d in data if d.get("success") and "payload" in d]

    if not successful:
        print("[yellow]Nema uspešnih payload-a za replay.[/yellow]")
        return

    print(f"[cyan]Ukupno pronađeno: {len(successful)} uspešnih payload-a[/cyan]")
    for i, p in enumerate(successful[:10]):
        print(f"[{i}] {p['payload']}")

    izbor = Prompt.ask("[bold green]Izaberi broj payload-a za replay[/bold green]", choices=[str(i) for i in range(len(successful[:10]))])
    target = Prompt.ask("[bold magenta]Unesi target URL (bez payload-a, npr. https://site.com/search?q=)[/bold magenta]")

    chosen = successful[int(izbor)]
    payload = chosen["payload"]
    full_url = target + payload

    try:
        r = requests.get(full_url, timeout=5)
        print(f"[green]Status:[/green] {r.status_code}")
        print(f"[blue]Response preview:[/blue]\n{r.text[:300]}...")
    except Exception as e:
        print(f"[red]Greška:[/red] {e}")

if __name__ == "__main__":
    replay()
