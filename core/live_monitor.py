from rich.console import Console
from rich.table import Table
from rich.live import Live
import time

class LiveMonitor:
    def __init__(self, targets, module_names):
        self.console = Console()
        self.targets = targets
        self.module_names = module_names
        self.status = {mod: "..." for mod in module_names}

    def update_status(self, module, result):
        self.status[module] = result

    def generate_table(self):
        table = Table(title="ShadowFox Live Skeniranje", expand=True)
        table.add_column("Modul", style="cyan", no_wrap=True)
        table.add_column("Status", style="magenta")

        for mod, status in self.status.items():
            table.add_row(mod, status)

        return table

    def start(self):
        with Live(self.generate_table(), refresh_per_second=4, console=self.console) as live:
            while any(v == "..." for v in self.status.values()):
                live.update(self.generate_table())
                time.sleep(0.5)
