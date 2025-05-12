import smtplib

class EmailSpoofFuzzer:
    def __init__(self):
        self.name = "Email Spoofing Fuzzer"
        self.payloads = [
            {"from": "admin@target.com", "to": "victim@target.com"},
            {"from": "support@target.com", "to": "victim@target.com"},
            {"from": "ceo@target.com", "to": "victim@target.com"}
        ]

    def run_tests(self, smtp_server):
        results = {}
        for payload in self.payloads:
            results[payload["from"]] = self.send_email(smtp_server, payload)
        return results

    def send_email(self, smtp_server, payload):
        try:
            server = smtplib.SMTP(smtp_server, 25, timeout=5)
            server.ehlo()
            response = server.sendmail(payload["from"], payload["to"], f"From: {payload['from']}\nTo: {payload['to']}\nSubject: Test\n\nThis is a spoof test.")
            server.quit()
            return "VULNERABLE: Spoofed email accepted" if not response else f"SAFE (partial rejection): {response}"
        except Exception as e:
            return f"SAFE: {str(e)}"
