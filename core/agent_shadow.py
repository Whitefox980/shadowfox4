from shadow_scan_core import ShadowScanCore

class ShadowAgent:
    def __init__(self, tools, target_url):
        self.tools = tools
        self.target = [target_url]

    def execute_plan(self):
        print("[AGENT] ShadowAgent pokreće testiranje alata...")
        scanner = ShadowScanCore(self.target)
        scanner.modules = self.tools  # koristi samo selektovane alate
        results = {}

        for module in scanner.modules:
            print(f"[AGENT] Pokrećem: {module.name}")
            result = module.run_tests(self.target)
            results[module.name] = result

        print("[AGENT] ShadowAgent završio sa testovima.")
        return results
