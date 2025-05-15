import time
import random
class StealthFuzzer:
    def __init__(self, target):
        self.target = target


    @staticmethod
    def random_delay(min_delay=0.4, max_delay=1.7):
        time.sleep(random.uniform(min_delay, max_delay))

    @staticmethod
    def fake_headers():
        return {
            "User-Agent": random.choice([...]),
            "Referer": "https://google.com",
            "Accept-Language": "en-US,en;q=0.9"
        }

    def simulate_traffic(self):
        print("[STEALTH] Počinjem maskirani saobraćaj...")
        fake_paths = ["/", "/contact", "/products"]
        for path in fake_paths:
            print(f"[-] Neuspešan stealth GET: {path}")
            self.random_delay()

