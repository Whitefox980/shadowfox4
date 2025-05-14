import random
import time
import requests

class StealthFuzzer:
    def __init__(self, target):
        self.target = target
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0)",
            "Mozilla/5.0 (Linux; Android 11)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2)",
            "curl/7.68.0"
        ]
        self.normal_paths = ["/", "/contact", "/about", "/products"]

    def simulate_traffic(self):
        print("[STEALTH] Počinjem maskirani saobraćaj...")
        for _ in range(random.randint(3, 6)):
            path = random.choice(self.normal_paths)
            headers = {"User-Agent": random.choice(self.user_agents)}
            try:
                requests.get(self.target + path, headers=headers, timeout=5)
                print(f"[+] Simuliran zahtev: {self.target+path}")
            except:
                print(f"[-] Neuspešan stealth GET: {path}")
            time.sleep(random.uniform(0.7, 2.0))

    def launch_payload(self, payload):
        headers = {"User-Agent": random.choice(self.user_agents)}
        try:
            full_url = self.target + f"?q={payload}"
            response = requests.get(full_url, headers=headers, timeout=5)
            return response.status_code, response.text
        except:
            return 0, ""
