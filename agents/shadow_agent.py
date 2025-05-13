from shadow_scan_core import ShadowScanCore
import json
from fuzzers import *
from core.ai_memory import AIMemory

class ShadowAgent:
    def __init__(self, attack_plan, target):
        self.attack_plan = attack_plan  # lista fuzz modula (instanci)
        self.target = target

    def execute_plan(self):
        results = {}
        for module in self.attack_plan:
            try:
                module_result = module.run_tests([self.target])
                results[module.name] = module_result
            except Exception as e:
                results[module.name] = f"ERROR: {str(e)}"
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
