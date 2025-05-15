# agents/kljucar.py

# === Stara verzija (kompatibilnost sa auto_mode.py) ===
def generate_plan(vectors, target="unknown"):
    return [{"vector": v, "signature": "default", "target": target} for v in vectors]

# === Nova verzija (AI planiranje) ===
class AIKljucar:
    def __init__(self, vectors, target):
        self.vectors = vectors
        self.target = target

    def generate(self):
        return [{"vector": v, "signature": self._choose_signature(v), "target": self.target} for v in self.vectors]

    def _choose_signature(self, vector):
        if vector == "SQL Injection":
            return "time-based"
        elif vector == "XSS":
            return "reflected"
        elif vector == "SSRF":
            return "metadata probe"
        elif vector == "LFI":
            return "file probe"
        return "default"
