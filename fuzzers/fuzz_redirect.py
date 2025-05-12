import requests

class RedirectFuzzer:
    def __init__(self):
        self.name = "Open Redirect Fuzzer"
        self.payloads = [
            "http://evil.com",
            "https://phishing-site.com",
            "//attacker.com",
            "/\\evil.com",        # Unicode bypass
            "///evil.com",        # Scheme-relative
        ]
        self.malicious_domains = ["evil.com", "phishing-site.com", "attacker.com"]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                test_url = f"{target}?redirect={payload}"
                status, redirected_url = self.send_request(test_url)
                is_vulnerable = self.analyze_redirect(redirected_url)
                results[test_url] = {
                    "status": status,
                    "redirected_to": redirected_url,
                    "vulnerable": is_vulnerable
                }
        return results

    def send_request(self, url):
        try:
            response = requests.get(url, timeout=5, allow_redirects=True)
            return response.status_code, response.url
        except requests.exceptions.RequestException:
            return "ERROR", "No response"

    def analyze_redirect(self, redirected_url):
        for domain in self.malicious_domains:
            if domain in redirected_url:
                return True
        return False
