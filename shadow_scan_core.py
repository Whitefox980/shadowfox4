from fuzzers.fuzz_sql import SQLFuzzer
from fuzzers.fuzz_xss import XSSFuzzer
from fuzzers.fuzz_lfi import LFIFuzzer
from fuzzers.fuzz_cmd import CMDFuzzer
from fuzzers.fuzz_traversal import TraversalFuzzer
from fuzzers.fuzz_rfi import RFIFuzzer
from fuzzers.fuzz_ssrf import SSRFFuzzer
from fuzzers.fuzz_redirect import RedirectFuzzer
from fuzzers.fuzz_cors import CORSFuzzer
from fuzzers.fuzz_host_header import HostHeaderFuzzer
from fuzzers.fuzz_csrf import CSRFFuzzer
from fuzzers.fuzz_xxe import XXEFuzzer
from fuzzers.fuzz_ldap import LDAPFuzzer
from fuzzers.fuzz_jwt import JWTFuzzer
from fuzzers.fuzz_http_methods import HTTPMethodsFuzzer
from fuzzers.fuzz_email_spoof import EmailSpoofFuzzer
from fuzzers.fuzz_dns_hijack import DNSHijackFuzzer
from fuzzers.fuzz_buffer_overflow import BufferOverflowFuzzer
from fuzzers.fuzz_side_channel import SideChannelFuzzer
from fuzzers.fuzz_race_condition import RaceConditionFuzzer
from fuzzers.fuzz_padding_oracle import PaddingOracleFuzzer
from fuzzers.fuzz_web_cache_poisoning import WebCachePoisoningFuzzer
from fuzzers.fuzz_log_injection import LogInjectionFuzzer
from fuzzers.fuzz_rce import RCEFuzzer
from fuzzers.fuzz_time_sql import TimeSQLFuzzer
from fuzzers.fuzz_heap_overflow import HeapOverflowFuzzer
from fuzzers.fuzz_subdomain_takeover import SubdomainTakeoverFuzzer
from fuzzers.fuzz_nosql import NoSQLFuzzer

class ShadowScanCore:
    def __init__(self, targets):
        self.targets = targets
        self.modules = [
            SQLFuzzer(), XSSFuzzer(), LFIFuzzer(), CMDFuzzer(),
            TraversalFuzzer(), RFIFuzzer(), SSRFFuzzer(), RedirectFuzzer(),
            CORSFuzzer(), HostHeaderFuzzer(), CSRFFuzzer(), XXEFuzzer(),
            LDAPFuzzer(), JWTFuzzer(), HTTPMethodsFuzzer(), EmailSpoofFuzzer(),
            DNSHijackFuzzer(), BufferOverflowFuzzer(), SideChannelFuzzer(),
            RaceConditionFuzzer(), PaddingOracleFuzzer(), WebCachePoisoningFuzzer(),
            LogInjectionFuzzer(), RCEFuzzer(), TimeSQLFuzzer(), HeapOverflowFuzzer(),
            SubdomainTakeoverFuzzer(), NoSQLFuzzer()
        ]

    def run_fuzz_tests(self):
        results = {}
        for module in self.modules:
            results[module.name] = module.run_tests(self.targets)
        return results
