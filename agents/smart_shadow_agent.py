import json
import random
from core.ai_brain import AIBrain
from core.mutation_engine import MutationEngine
from fuzzers.adaptive_fuzzer import AdaptiveFuzzer

class SmartShadowAgent:
    def __init__(self,meta, history_file="data/mission_history.json"):
        self.history_file = history_file
        self.meta = meta
        self.ai_brain = AIBrain(self.meta)
        self.ai_brain = AIBrain(meta)  # ako već imaš `meta` iz prethodnog koraka
        self.engine = MutationEngine()
        self.attack_type = "XSS"  # ili "SQLi", po potrebi
        self.fuzzer = AdaptiveFuzzer(self.attack_type)
        self.target = None

    def load_history(self):
        try:
            with open(self.history_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def analyze_results(self, results):
        if not results:
            return ["basic_test_payload"]

        successful_payloads = []
        for r in results:
            if isinstance(r, dict) and r.get("success") and "payload" in r:
                successful_payloads.append(r["payload"])
        return successful_payloads if successful_payloads else ["basic_test_payload"]

    def sort_successful_payloads(self, results, top_n=10):
        """
        Sortira uspešne payload-e po dužini (kraći su često bolji) i uklanja duplikate.
        Vraća listu top N jedinstvenih pogodaka.
        """
        successful = [r for r in results if isinstance(r, dict) and r.get("success")]
        unique = {r["payload"]: r for r in successful}
        sorted_hits = sorted(unique.values(), key=lambda x: len(x["payload"]))
        return sorted_hits[:top_n]
    def mutate_payloads(self, payloads):
        mutated_payloads = []
        for payload in payloads:
            mutated_payloads.extend(self.engine.mutate_payload(payload))
        return list(set(mutated_payloads))

    def generate_attack_plan(self, target):
        history = self.load_history()
        target_history = history.get(target, [])
        best_payloads = self.analyze_results(target_history)
        enhanced_payloads = self.mutate_payloads(best_payloads)

        attack_plan = {
            "target": target,
            "vector": self.ai_brain.plan(),
            "payloads": enhanced_payloads
        }
        return attack_plan

    def run(self):
        attack_plan = self.generate_attack_plan(self.target)
        results = self.fuzzer.fuzz_target(self.target)
        self.save_results(attack_plan["target"], results)
        print(f"[SMART] Završeno skeniranje sa {len(results)} payload-a.")
        # Automatsko sortiranje uspešnih payload-a
        sorted_hits = self.sort_successful_payloads(results, top_n=10)
        print("\n[SMART] Top 10 pogodaka:")
        for i, hit in enumerate(sorted_hits, 1):
            print(f"{i}. {hit['payload']}")
    def test_payload(self, target, payload):
        return random.choice([True, False])

    def save_results(self, target, results):
        try:
            with open(self.history_file, "r") as file:
                history = json.load(file)
        except FileNotFoundError:
            history = {}

        if target not in history:
            history[target] = []
        history[target].extend(results)

        with open(self.history_file, "w") as file:
            json.dump(history, file, indent=2)

        self.write_stats_file(target, results)
        # Dodaj i zapis uspešnih payload-a za fuzz_history.json
        successful = [r for r in results if r["success"]]
        if successful:
            fuzz_path = "data/fuzz_history.json"
            try:
                with open(fuzz_path, "r") as f:
                     fuzz_log = json.load(f)
            except:
                fuzz_log = {}

            if self.attack_type not in fuzz_log:
                fuzz_log[self.attack_type] = []

                fuzz_log[self.attack_type].extend(successful)

            with open(fuzz_path, "w") as f:
                json.dump(fuzz_log, f, indent=2)
    def write_stats_file(self, target, results):
        stats = {}
        for entry in results:
            key = entry["payload"][:30]
            stats[key] = "Success" if entry["success"] else "Fail"

        try:
            with open("data/attack_stats.json", "r") as f:
                existing = json.load(f)
        except FileNotFoundError:
            existing = {}

        existing[target] = stats

        with open("data/attack_stats.json", "w") as f:
            json.dump(existing, f, indent=2)
from datetime import datetime

def save_results(self, target, results):
    # ... postojeći kod ...

    # Shadow signature zapis
    sig_path = f"data/signatures/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{target.replace('/', '_')}.sig"
    os.makedirs("data/signatures", exist_ok=True)
    with open(sig_path, "w") as sig:
        sig.write(f"ShadowFox v4\n")
        sig.write(f"Target: {target}\n")
        sig.write(f"Payloads: {len(results)}\n")
        sig.write(f"Author: CUPKO-AI\n")
        sig.write(f"SignatureID: {hash(target + str(datetime.now())) % 999999999}\n")
