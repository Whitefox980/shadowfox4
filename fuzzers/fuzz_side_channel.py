import time
import requests

class SideChannelFuzzer:
    def __init__(self):
        self.name = "Side-Channel Attack Fuzzer"
        self.payloads = ["admin", "password123", "123456", "root", "guest"]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            response_times = []
            for payload in self.payloads:
                t = self.measure_response_time(target, payload)
                response_times.append((payload, t))
            results[target] = self.analyze_times(response_times)
        return results

    def measure_response_time(self, url, payload):
        start = time.time()
        try:
            requests.post(url, data={"password": payload}, timeout=5)
        except requests.exceptions.RequestException:
            return -1
        return round(time.time() - start, 5)

    def analyze_times(self, times):
        valid = [t for p, t in times if t > 0]
        if not valid:
            return "ERROR: No valid timings"
        deviation = max(valid) - min(valid)
        return {
            "min": min(valid),
            "max": max(valid),
            "deviation": round(deviation, 5),
            "vulnerable": deviation > 0.1  # prag za sumnjivu varijaciju
        }
