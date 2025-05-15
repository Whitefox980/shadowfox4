# core/ai_brain.py

import os
import json

# === Nova klasa ===
class BrainSuggestion:
    def __init__(self, metadata):
        self.metadata = metadata
        self.api_key = os.getenv("OPENAI_API_KEY")

    def plan(self):
        from core.strateg import Strateg
        strategy = Strateg()
        priority = strategy.get_priority_modules(min_success_rate=30)
        if priority:
            print(f"[AI BRAIN] Strateg preporučuje: {priority}")
            return priority
        return self._ask_openai()

    def _ask_openai(self):
        import openai
        openai.api_key = self.api_key

        prompt = f"""
Na osnovu sledećih meta podataka, predloži do 3 modula napada (kao JSON niz):
Title: {self.metadata.get("title")}
Opis: {self.metadata.get("meta_description")}
Linkovi: {self.metadata.get("links")}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50
            )
            reply = response.choices[0].message.content
            return self._extract_modules(reply)
        except:
            return ["SQL Injection", "XSS"]

    def _extract_modules(self, text):
        try:
            return json.loads(text)
        except:
            return ["SQL Injection", "XSS"]

# === Stara funkcija ===
def suggest_vectors(meta):
    platform = meta.get("platform", "").lower()

    if "wordpress" in platform:
        return ["XSS", "SQL Injection", "LFI"]
    elif "node" in platform:
        return ["XSS", "SSRF"]
    elif "php" in platform:
        return ["LFI", "SQL Injection"]
    else:
        return ["XSS", "SSRF", "SQL Injection", "LFI"]


# === Dummy klasa za stare pozive ===
class AIBrain:
    def __init__(self, meta):
        self.meta = meta

    def suggest_vectors(self):
        return suggest_vectors(self.meta)
