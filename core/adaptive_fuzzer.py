from fuzzers.xss_fuzzer import XSSFuzzer
from fuzzers.sql_fuzzer import SQLiFuzzer
from fuzzers.ssrf_fuzzer import SSRFFuzzer
from fuzzers.lfi_fuzzer import LFIFuzzer

class AdaptiveFuzzer:
    def __init__(self, vector):
        self.vector = vector.lower()

    def fuzz_target(self, target):
        if self.vector == "xss":
            return XSSFuzzer().fuzz_target(target)
        elif self.vector == "sql injection":
            return SQLiFuzzer().fuzz_target(target)
        elif self.vector == "ssrf":
            return SSRFFuzzer().fuzz_target(target)
        elif self.vector == "lfi":
            return LFIFuzzer().fuzz_target(target)
        else:
            print(f"[WARN] Nepoznat vektor: {self.vector}")
            return []



