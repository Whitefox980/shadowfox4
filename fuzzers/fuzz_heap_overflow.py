import requests

class HeapOverflowFuzzer:
    def __init__(self):
        self.name = "Heap Overflow Fuzzer"
        self.payloads = [
            "A" * 50000,
            "B" * 100000,
            "C" * 200000
        ]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                response = self.send_request(target, payload)
                results[f"{target} ({len(payload)} bytes)"] = response
        return results

    def send_request(self, url, payload):
        try:
            response = requests.post(url, data={"input": payload}, timeout=5)
            if response.status_code == 500:
                return "VULNERABLE"
            return "SAFE"
        except requests.exceptions.RequestException:
            return "ERROR"
