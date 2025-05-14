# agents/shadow_agent.py

class ShadowAgent:
    def __init__(self, modules, target):
        self.modules = modules  # lista dict-ova: {name, payloads}
        self.target = target
        self.results = {}

    def execute_plan(self):
        for module in self.modules:
            name = module.get("name", "Unknown")
            payloads = module.get("payloads", [])

            if not payloads:
                self.results[name] = "NO PAYLOADS"
                continue

            self.results[name] = []
            for payload in payloads:
                test_url = f"{self.target}?vuln={payload}"
                self.results[name].append(test_url)

        return self.results
