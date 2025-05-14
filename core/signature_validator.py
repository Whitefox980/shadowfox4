import hashlib

class SignatureValidator:
    def __init__(self, salt="shadowfox"):
        self.salt = salt

    def generate_signature(self, payload, timestamp, vector):
        """Kreira potpis na osnovu payload-a, vremena i vektora"""
        base = f"{payload}|{timestamp}|{vector}|{self.salt}"
        return hashlib.sha256(base.encode()).hexdigest()

    def validate(self, payload, timestamp, vector, signature):
        """Proverava da li potpis odgovara datim podacima"""
        expected = self.generate_signature(payload, timestamp, vector)
        return expected == signature
