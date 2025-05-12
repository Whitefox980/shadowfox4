import requests

class PaddingOracleFuzzer:
    def __init__(self):
        self.name = "Padding Oracle Attack Fuzzer"
        self.payloads = [
            "dGVzdDE=",  # test base64
            "ZmFrZUJsb2NrMQ==",  # fake block1
            "d3JvbmdQYWRkaW5n==",  # wrong padding
            "cGFkaW5nZXJyb3I=",  # triggers 'padding error'
        ]
        self.signatures = [
            "padding error", "invalid padding", "bad decrypt", "decryption failed", "block length"
        ]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                status, response_text = self.send_request(target, payload)
                vulnerable = self.analyze_response(response_text)
                results[f"{target} | Payload={payload}"] = {
                    "status": status,
                    "vulnerable": vulnerable
                }
        return results

    def send_request(self, url, payload):
        try:
            response = requests.post(url, data={"ciphertext": payload}, timeout=5)
            return response.status_code, response.text[:1000]
        except requests.exceptions.RequestException:
            return "ERROR", "No response"

    def analyze_response(self, text):
        for sig in self.signatures:
            if sig.lower() in text.lower():
                return True
        return False
