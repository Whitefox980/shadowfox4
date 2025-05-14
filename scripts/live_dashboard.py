def start_dashboard():
    console = Console()
    console.clear()
    console.rule("[bold green]ShadowFox Dashboard")

    data = load_results()

    if not data:
        console.print("[red]Nema rezultata za prikaz.")
        return

    for target, results in data.items():
        console.print(f"\n[bold cyan]Meta:[/bold cyan] {target}")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Modul", width=20)
        table.add_column("Broj Payload-a", justify="center")
        table.add_column("Status", justify="center")

        # NOVI FORMAT
        if isinstance(results, dict):
            for modul, payloads in results.items():
                if isinstance(payloads, list):
                    status = "Završeno"
                    count = str(len(payloads))
                elif isinstance(payloads, str):
                    status = payloads
                    count = "0"
                else:
                    status = "Nepoznat format"
                    count = "?"
                table.add_row(modul, count, status)

        # STARI FORMAT
        elif isinstance(results, list):
            table.add_row("Legacy Log", str(len(results)), "Lista payload-a")

        console.print(table)
