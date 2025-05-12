from shadow_scan_core import ShadowScanCore
import json
from fuzzers import *
from core.ai_memory import AIMemory

class ShadowAgent:
    def __init__(self, attack_plan, targets):
        self.attack_plan = attack_plan
        self.targets = targets
        self.memory = AIMemory()

    def execute_plan(self):
        results = {}

        for module_name, module_list in self.attack_plan.items():
            for mod in module_list:
                fuzz_module = self.load_fuzzer(mod)
                if not fuzz_module:
                    continue

                print(f"[ShadowAgent] Pokrećem modul: {mod}")
                result = fuzz_module.run_tests(self.targets)
                results[mod] = result

                # Ako detektovana ranjivost → beleži kao uspešan
                for verdict in result.values():
                    if isinstance(verdict, str) and "VULNERABLE" in verdict:
                        self.memory.record_success(mod)

        self.memory.remember_mission(results)
        self.memory.save()
        return results

    def load_fuzzer(self, mod_name):
        fuzz_map = {
            "SQL Injection": SQLFuzzer,
            "XSS": XSSFuzzer,
            "LFI": LFIFuzzer,
            "CMD": CMDFuzzer,
            "Traversal": TraversalFuzzer,
            "RFI": RFIFuzzer,
            "SSRF": SSRFFuzzer,
            "Redirect": RedirectFuzzer,
            "CORS": CORSFuzzer,
            "HostHeader": HostHeaderFuzzer,
            "CSRF": CSRFFuzzer,
            "XXE": XXEFuzzer,
            "LDAP": LDAPFuzzer,
            "JWT": JWTFuzzer,
            "HTTPMethods": HTTPMethodsFuzzer,
            "EmailSpoof": EmailSpoofFuzzer,
            "DNSHijack": DNSHijackFuzzer,
            "BufferOverflow": BufferOverflowFuzzer,
            "SideChannel": SideChannelFuzzer,
            "RaceCondition": RaceConditionFuzzer,
            "PaddingOracle": PaddingOracleFuzzer,
            "CachePoison": WebCachePoisoningFuzzer,
            "LogInjection": LogInjectionFuzzer,
            "RCE": RCEFuzzer,
            "TimeSQL": TimeSQLFuzzer,
            "HeapOverflow": HeapOverflowFuzzer,
            "SubdomainTakeover": SubdomainTakeoverFuzzer,
            "NoSQL": NoSQLFuzzer
        }

        klass = fuzz_map.get(mod_name.replace(" ", "").replace("-", ""))
        return klass() if klass else None
