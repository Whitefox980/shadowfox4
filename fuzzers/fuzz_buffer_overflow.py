import requests

class BufferOverflowFuzzer:
    def __init__(self):
        self.name = "Buffer Overflow Fuzzer"
        self.payloads = [
            "A" * 5000,
            "B" * 10000,
            "C" * 20000,
            "%n" * 1000,  # potencijalni format string injection
            "\x90" * 3000  # NOP sled za detekciju shellcode-friendly bafera
        ]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                status, response = self.send_request(target, payload)
                vulnerable = self.analyze_response(response)
                results[f"{target} | {len(payload)} bytes"] = {
                    "status": status,
                    "vulnerable": vulnerable
                }
        return results

    def send_request(self, url, payload):
        try:
            response = requests.post(url, data={"input": payload}, timeout=5)
            return response.status_code, response.text[:1000]
        except requests.exceptions.RequestException:
            return "ERROR", "No response"

    def analyze_response(self, text):
        return any(error in text.lower() for error in ["segmentation fault", "buffer overflow", "memory error", "core dumped"])
