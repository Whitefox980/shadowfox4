import requests

class CORSFuzzer:
    def __init__(self):
        self.name = "CORS Misconfiguration Fuzzer"
        self.payloads = [
            {"Origin": "https://evil.com"},
            {"Origin": "https://attacker.com"},
            {"Origin": "null"}
        ]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for headers in self.payloads:
                status, resp_headers = self.send_request(target, headers)
                vulnerable = self.analyze_headers(headers, resp_headers)
                results[f"{target} | Origin: {headers['Origin']}"] = {
                    "status": status,
                    "vulnerable": vulnerable,
                    "allowed_origin": resp_headers.get("Access-Control-Allow-Origin", "N/A")
                }
        return results

    def send_request(self, url, headers):
        try:
            response = requests.get(url, headers=headers, timeout=5)
            return response.status_code, response.headers
        except requests.exceptions.RequestException:
            return "ERROR", {}

    def analyze_headers(self, sent_headers, response_headers):
        origin = sent_headers.get("Origin", "")
        allowed = response_headers.get("Access-Control-Allow-Origin", "")
        return allowed == origin or allowed == "*"
