import random
import json
import requests
from core.mutation_engine import MutationEngine
from core.stealth import StealthFuzzer
class AdaptiveFuzzer:
    def __init__(self, attack_type, history_file="data/fuzz_history.json"):
        self.history_file = history_file
        self.engine = MutationEngine()

        # Fleksibilno rešavanje imena vektora
        if isinstance(attack_type, dict):
            self.attack_type = attack_type.get("vector", "unknown").lower()
        else:
            self.attack_type = str(attack_type).lower()

        self.vector = self.attack_type  # kompatibilno za obe verzije

    def load_history(self):
        try:
            with open(self.history_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def get_successful_payloads(self, history):
        return [h["payload"] 
        for h in history if h.get("success") and self.attack_type in h.get("vector", "")]
    def evolve_payloads(self, payloads):
        evolved = [self.engine.mutate_payload(p) for p in payloads]
        return [item for sublist in evolved for item in sublist]
    def test_payload(self, target, payload):
        headers = StealthFuzzer.fake_headers()
        try:
            response = requests.get(target, headers=headers, params={"q": payload}, timeout=5)
            response_text = response.text.lower()
            response_code = response.status_code
            success = "error" in response_text or response_code >= 500
            return success, response_text
        except:
            StealthFuzzer.random_delay()
            return False, ""
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
                success, response_text = self.test_payload(target, payload)
                db_type = self.engine.detect_db_type(response_text)
                adapted = self.engine.adapt_to_environment(db_type)

                results.append({
                    "payload": payload,
                    "success": success,
                    "db_type": db_type,
                    "adapted_payload": adapted
                })

            return results
