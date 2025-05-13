import random
import json
import requests
from core.mutation_engine import MutationEngine
from core.stealth import random_delay, fake_headers

class AdaptiveFuzzer:
    def __init__(self, attack_type, history_file="data/fuzz_history.json"):
        self.attack_type = attack_type
        self.engine = MutationEngine()
        self.history_file = history_file

    def load_history(self):
        try:
            with open(self.history_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def get_successful_payloads(self, history):
        return [h["payload"] for h in history.get(self.attack_type, []) if h["success"]]

    def evolve_payloads(self, payloads):
        evolved = [self.engine.mutate_payload(p) for p in payloads]
        return [item for sublist in evolved for item in sublist]

    def test_payload(self, target, payload):
        headers = fake_headers()
        try:
            response = requests.get(target, headers=headers, params={"q": payload}, timeout=5)
            success = "error" in response.text.lower() or response.status_code >= 500
        except:
            success = False
        random_delay()
        return success

    def fuzz_target(self, target):
        history = self.load_history()
        best_payloads = self.get_successful_payloads(history)
        base_payloads = best_payloads if best_payloads else [self.engine.generate_payload(self.attack_type)]

        history_payloads = self.engine.load_successful_history(self.attack_type)
        if history_payloads:
            payloads = self.evolve_payloads(history_payloads)
        else:
            payloads = [self.engine.generate_payload(self.attack_type)]
        results = []
        for payload in payloads:
            success = self.test_payload(target, payload)
            results.append({"payload": payload, "success": success})
        return results
