# core/smart_shadow_agent.py

import random
import json
from core.memory import MissionMemory
from core.ai_brain import BrainSuggestion
from datetime import datetime
from fuzzers.adaptive_fuzzer import AdaptiveFuzzer
import hashlib
from datetime import datetime
from fuzzers.stealth_fuzzer import StealthFuzzer
from agents.mission_memory import MissionMemory
from core.send_attack import send_attack
class SmartShadowAgent:
from core.mutation_engine import MutationEngine
from core.dynamic_mutator import DynamicPayloadMutator
from core.stealth import StealthFuzzer
from core.adaptive_fuzzer import AdaptiveFuzzer

class SmartShadowAgent:
    def __init__(self):
        self.engine = MutationEngine()
        self.mutator = DynamicPayloadMutator()
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
    def run(self, target, modules):
            print(f"[Agent] Pokrećem napad na: {target} sa modulima: {modules}")
            print(f"[EXEC] Pokrećem AI napad na metu: {target}")

            self.target = target
            stealth = StealthFuzzer(self.target)
            stealth.simulate_traffic()
            attack_plan = self.generate_attack_plan(target)
            results = []

            for vector in attack_plan["payloads"]:
                fuzzer = AdaptiveFuzzer(vector)
                fuzz_results = fuzzer.fuzz_target(target)

                if not fuzz_results:
                    print(f"[!] Fuzzer nije vratio rezultate za vektor: {vector}")
                    continue  # preskoči ovaj vektor

                for r in fuzz_results:
                    results.append({
                        "payload": r["payload"],
                        "success": r["success"],
                        "signature": {
                            "vector": vector,
                            "agent": "CUPKO-AI",
                            "timestamp": datetime.now().isoformat(),
                            "hash": hashlib.sha256(r["payload"].encode()).hexdigest()[:10]
                        }
                    })

                    final_payload = self.mutator.mutate_payload(r["payload"])
                    print(f"[Agent] Finalni payload ({vector}): {final_payload}")

                    status, resp_text = send_attack(target, final_payload)
                    final_payload = self.mutator.mutate_payload(final_payload, response_status=status, response_text=resp_text)
            self.save_results(target, results)
            print(f"[SMART] Završeno skeniranje sa {len(results)} payload-a.")
    def send_attack(target, payload):
            print(f"[EXEC] Slanjem payload-a na {target} ...")
            print(f"[EXEC] Payload: {payload}")
    # TODO: Integracija sa HTTP requesterima (requests, httpx itd.)
