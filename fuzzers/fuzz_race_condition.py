import requests
import threading

class RaceConditionFuzzer:
    def __init__(self):
        self.name = "Race Condition Fuzzer"
        self.payloads = [
            {"action": "withdraw", "amount": "1000"},
            {"action": "change_role", "role": "admin"}
        ]
        self.threads_per_payload = 5

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                key = f"{target} | {payload['action']}"
                results[key] = self.run_race_test(target, payload)
        return results

    def run_race_test(self, url, payload):
        threads = []
        responses = []

        def send():
            try:
                r = requests.post(url, data=payload, timeout=5)
                responses.append(r.text[:100])
            except:
                responses.append("ERROR")

        for _ in range(self.threads_per_payload):
            t = threading.Thread(target=send)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        vuln_hits = [r for r in responses if "success" in r.lower() or "admin" in r.lower()]
        if len(vuln_hits) > 1:
            return f"VULNERABLE: {len(vuln_hits)} success responses"
        return "SAFE"
