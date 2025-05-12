import requests

class HostHeaderFuzzer:
    def __init__(self):
        self.name = "Host Header Injection Fuzzer"
        self.payloads = [
            {"Host": "evil.com"},
            {"Host": "attacker.com"},
            {"Host": "localhost"},
            {"Host": "127.0.0.1"},
            {"Host": "internal.lan"}
        ]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for headers in self.payloads:
                status, response_text = self.send_request(target, headers)
                reflected = self.analyze_response(headers["Host"], response_text)
                results[f"{target} | Host: {headers['Host']}"] = {
                    "status": status,
                    "reflected": reflected
                }
        return results

    def send_request(self, url, headers):
        try:
            response = requests.get(url, headers=headers, timeout=5)
            return response.status_code, response.text[:1000]
        except requests.exceptions.RequestException:
            return "ERROR", "No response"

    def analyze_response(self, injected_host, response_text):
        return injected_host in response_text
