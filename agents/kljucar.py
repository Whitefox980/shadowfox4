import json
from core.shadow_core_log import log

class Kljucar:
    def __init__(self, analysis_data):  # Prima dict, više ne čita fajl
        self.analysis = analysis_data

    def generate_plan(self):
        plan = {
            "SQL Injection": False,
            "XSS": False,
            "LFI": False,
            "RFI": False,
            "SSRF": False,
            "CORS": False,
            "Open Redirect": False
        }

        links = self.analysis.get("links", [])
        meta = self.analysis.get("meta", "").lower()

        if any("id=" in link or "page=" in link for link in links):
            plan["SQL Injection"] = True
            plan["LFI"] = True

        if any("redirect" in link for link in links):
            plan["Open Redirect"] = True

        if "cross-site" in meta or "javascript" in meta:
            plan["XSS"] = True

        if "api" in meta or "internal" in meta:
            plan["SSRF"] = True

        if "file" in meta:
            plan["RFI"] = True

        if "access-control" in meta:
            plan["CORS"] = True

        log("Ključar", f"Planirana upotreba alata: {{ {', '.join(k for k, v in plan.items() if v)} }}")
        return plan
