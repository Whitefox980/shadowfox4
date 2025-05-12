import requests

class HTTPMethodsFuzzer:
    def __init__(self):
        self.name = "HTTP Method Manipulation Fuzzer"
        self.methods = ["OPTIONS", "TRACE", "DELETE", "PUT", "PATCH", "CONNECT"]
        self.sensitive_codes = [200, 201, 202, 204]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for method in self.methods:
                status, text = self.send_request(target, method)
                results[f"{target} ({method})"] = {
                    "status": status,
                    "vulnerable": status in self.sensitive_codes,
                    "message": f"{method} allowed" if status in self.sensitive_codes else "Not allowed"
                }
        return results

    def send_request(self, url, method):
        try:
            response = requests.request(method, url, timeout=5)
            return response.status_code, response.text[:500]
        except requests.exceptions.RequestException:
            return "ERROR", "No response"
