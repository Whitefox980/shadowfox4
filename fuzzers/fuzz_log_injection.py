import requests

class LogInjectionFuzzer:
    def __init__(self):
        self.name = "Log Injection Fuzzer"
        self.payloads = [
            "Normal operation\nERROR: Unauthorized Access",
            "User failed login\nInjected Log: Root Access Granted",
            "'; DROP TABLE logs; --",
            "INFO: Session closed\nALERT: Privilege Escalated",
            "[LOG] End\n[ALERT] Admin override triggered"
        ]
        self.signatures = ["unauthorized", "admin", "override", "alert", "granted", "error", "escalated"]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                status, text = self.send_request(target, payload)
                suspicious = self.analyze_response(text)
                results[f"{target} | {payload[:20]}..."] = {
                    "status": status,
                    "vulnerable": suspicious
                }
        return results

    def send_request(self, url, payload):
        try:
            response = requests.post(url, data={"log_entry": payload}, timeout=5)
            return response.status_code, response.text[:1000]
        except requests.exceptions.RequestException:
            return "ERROR", "No response"

    def analyze_response(self, text):
        for sig in self.signatures:
            if sig.lower() in text.lower():
                return True
        return False
