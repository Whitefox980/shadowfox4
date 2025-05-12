import openai

class AIKljucar:
    def __init__(self, metadata):
        self.metadata = metadata
        self.tools_db = {
            "SQL": "SQL Injection Fuzzer",
            "login": "BruteForce Tester",
            "form": "XSS Fuzzer",
            "upload": "RCE Fuzzer",
            "admin": "Auth Bypass Fuzzer",
            "token": "JWT Fuzzer",
            "file": "LFI/RFI Fuzzer",
            "api": "SSRF Fuzzer"
        }

    def decide_tools(self):
        prompt = f"""
Ti si AI analitičar za etičko hakovanje.
Na osnovu sledeće analize sajta odluči koji fuzz moduli treba da se koriste.

TITLE: {self.metadata.get('title')}
META: {self.metadata.get('meta')}
LINKOVI: {self.metadata.get('links')[:5]}

Vrati samo spisak modula iz baze: {list(self.tools_db.values())}
Ništa drugo ne prikazuj.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            return response.choices[0].message.content.strip().split("\n")
        except Exception as e:
            return [f"ERROR: {e}"]
