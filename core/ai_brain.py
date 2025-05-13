import os
import openai

class BrainSuggestion:
    def __init__(self, metadata):
        self.metadata = metadata
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def plan(self):
        prompt = f"""
Analiziraj sledeće metapodatke o sajtu i predloži koji fuzz moduli treba da se pokrenu (izaberi do 5):

Title: {self.metadata.get("title")}
Description: {self.metadata.get("meta_description")}
Links: {', '.join(self.metadata.get("links", [])[:5])}

Moduli koje možeš izabrati:
- SQL Injection
- XSS
- LFI
- RFI
- SSRF
- CMD Injection
- Open Redirect
- CSRF
- CORS
- JWT
- XXE
- DNS Hijack
- Buffer Overflow
- Race Condition
- NoSQL Injection
- Host Header Injection
- Web Cache Poisoning
- Log Injection
- Time-Based SQLi
- RCE
- HTTP Method
- LDAP

Vrati listu samo imena modula u JSON nizu.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Ti si AI sigurnosni analitičar."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            text = response.choices[0].message.content.strip()
            return self._extract_modules(text)

        except Exception as e:
            return ["SQL Injection", "XSS", "LFI"]  # fallback

    def _extract_modules(self, text):
        import json
        try:
            return json.loads(text)
        except:
            return ["SQL Injection", "XSS"]
