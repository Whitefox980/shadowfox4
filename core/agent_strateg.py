import json
import os
from datetime import datetime
import openai

class Strateg:
    def __init__(self):
        self.history_path = "data/mission_history.json"
        self.plan_path = "data/next_plan.json"

    def generate_strategy(self, results):
        print("[STRATEG] Analiziram rezultate za učenje...")

        summary = self.build_summary(results)
        self.save_to_history(summary)

        prompt = self.build_prompt(summary)
        plan = self.ask_openai(prompt)

        with open(self.plan_path, "w") as f:
            json.dump(plan, f, indent=2)

        print("[STRATEG] Sledeći AI plan sačuvan u next_plan.json")

    def build_summary(self, results):
        summary = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "modules_used": list(results.keys()),
            "vulnerabilities": []
        }

        for mod, output in results.items():
            if isinstance(output, dict):
                vulns = [k for k, v in output.items() if "VULNERABLE" in str(v)]
                summary["vulnerabilities"].extend(vulns)

        return summary

    def save_to_history(self, summary):
        if os.path.exists(self.history_path):
            with open(self.history_path) as f:
                history = json.load(f)
        else:
            history = []

        history.append(summary)
        with open(self.history_path, "w") as f:
            json.dump(history, f, indent=2)

    def build_prompt(self, summary):
        return f"""
Ti si strateg za AI hakerski sistem. Na osnovu prethodnih rezultata:

Vreme: {summary['timestamp']}
Moduli: {summary['modules_used']}
Ranjivosti: {summary['vulnerabilities']}

Izaberi koji fuzz moduli bi trebalo da se pokrenu u sledećoj misiji. Vrati samo listu naziva fuzzera.
"""

    def ask_openai(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            tools = response.choices[0].message.content.strip().split("\n")
            return {name: True for name in tools}
        except Exception as e:
            print(f"[STRATEG] AI Greška: {e}")
            return {}
