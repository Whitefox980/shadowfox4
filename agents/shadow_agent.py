# agents/shadow_agent.py

from fuzzers import *

class ShadowAgent:
    def __init__(self, modules, target):
        self.modules = modules  # lista dict-ova: {name, payloads}
        self.target = target
        self.results = {}

    def execute_plan(self):
        for module in self.modules:
            try:
                name = module.get("name")
                payloads = module.get("payloads", [])

                fuzz_instance = self.load_fuzzer(name)
                if fuzz_instance is None:
                    self.results[name] = f"{name} not implemented"
                    continue

                fuzz_instance.set_target(self.target)
                fuzz_instance.set_payloads(payloads)

                tested_payloads = []
                for p in payloads:
                    # Ovo simulira pravi napad — upiši ovde pravu logiku kad budeš imao
                    tested_payloads.append(f"{self.target}?p={p}")

                self.results[name] = tested_payloads

            except Exception as e:
                self.results[name] = f"ERROR: {str(e)}"

        return self.results

    def load_fuzzer(self, mod_name):
        fuzz_map = {
            "SQL Injection": SQLFuzzer,
            "XSS": XSSFuzzer,
            "LFI": LFIFuzzer,
        }
        klass = fuzz_map.get(mod_name)
        return klass() if klass else None
