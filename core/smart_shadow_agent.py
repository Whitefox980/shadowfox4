# core/smart_shadow_agent.py

import random
import json
from core.mutation_engine import MutationEngine
from core.memory import MissionMemory
from core.ai_brain import BrainSuggestion
from datetime import datetime
from fuzzers.adaptive_fuzzer import AdaptiveFuzzer

class SmartShadowAgent:
    def __init__(self):
        self.engine = MutationEngine()
        self.history_file = "data/payload_results.json"

    def generate_attack_plan(self, target):
        metadata = {
            "title": "Test aplikacija",
            "meta_description": "Prikaz korisnika i login forma",
            "links": ["/login", "/profile", "/search"]
        }

        brain = BrainSuggestion(metadata)
        attack_vectors = brain.plan()  # npr. ['SQL Injection', 'XSS']

        all_payloads = []
        for vector in attack_vectors:
        fuzzer = AdaptiveFuzzer(vector)
        fuzz_results = fuzzer.fuzz_target(target)
        for fr in fuzz_results:
            all_payloads.append(fr)

        return {"target": target, "payloads": all_payloads}
    def test_payload(self, target, payload):
        # OVDE ide prava logika kasnije
        return random.choice([True, False])  # simulacija

    def save_results(self, target, results):
        try:
            with open(self.history_file, "r") as file:
                history = json.load(file)
                if not isinstance(history, dict):
                    history = {}
        except:
            history = {}

        existing = history.get(target, [])
        if not isinstance(existing, list):
            existing = []

        existing.extend(results)
        history[target] = existing

        with open(self.history_file, "w") as file:
            json.dump(history, file, indent=2)

    # Takođe pamti kao misiju
        mission = {
            "target": target,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "results": {r["payload"]: r["success"] for r in results}
        }

        mem = MissionMemory()
        mem.remember_mission(mission)

    def run(self, target):
        """Kompletna rutina: AI bira napad, mutira i testira"""
        print(f"[SMART] Pokrećem AI napad na metu: {target}")
        attack_plan = self.generate_attack_plan(target)
        results = attack_plan["payloads"]  # već sadrži success info

        for payload in attack_plan["payloads"]:
            success = self.test_payload(attack_plan["target"], payload)
            results.append({"payload": payload, "success": success})
        self.save_results(target, results)
        print(f"[SMART] Završeno skeniranje sa {len(results)} payload-a.")
