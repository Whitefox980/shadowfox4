import random

class DynamicPayloadMutator:
    def __init__(self):
        pass

    def mutate_payload(self, payload, response_status=None, response_text=""):
        """
        Prilagođava payload na osnovu odgovora servera
        - Ako je 403: encoduje i dodaje bypass trikove
        - Ako je 500: menja strukturu (npr. escape)
        - Ako je reflektovan u odgovoru: ubacuje dodatne elemente
        """
        if not isinstance(payload, str):
            return payload  # Za sada obrađujemo samo string payload-e

        if response_status == 403:
            return self._encode_payload(payload)

        elif response_status == 500:
            return self._obfuscate(payload)

        elif payload in response_text:
            return self._inject_reflection(payload)

        # Ako ništa nije pogođeno, vrati neizmenjen payload
        return payload

    def _encode_payload(self, payload):
        return ''.join(['%%%02x' % ord(c) for c in payload])

    def _obfuscate(self, payload):
        return payload.replace("=", " LIKE ").replace(" OR ", " || ")

    def _inject_reflection(self, payload):
        suffix = random.choice(["//", "#", "--", "/*exploit*/"])
        return f"{payload}{suffix}"
