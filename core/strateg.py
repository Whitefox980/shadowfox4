import json
from core.memory import MissionMemory

class Strateg:
    def __init__(self):
        self.memory = MissionMemory()

    def analyze(self):
        missions = self.memory.get_all_missions()
        if not missions:
            print("[STRATEG] Nema dovoljno misija za analizu.")
            return {}

        stats = {}
        for mission in missions:
            for payload, success in mission.get("results", {}).items():
                attack_type = self.detect_attack_type(payload)
                if attack_type not in stats:
                    stats[attack_type] = {"hits": 0, "total": 0}
                stats[attack_type]["total"] += 1
                if success:
                    stats[attack_type]["hits"] += 1

        return stats

    def detect_attack_type(self, payload):
        if "script" in payload or "alert" in payload:
            return "XSS"
        if "'" in payload or " OR " in payload:
            return "SQLi"
        if "127.0.0.1" in payload:
            return "SSRF"
        if isinstance(payload, dict) and "role" in payload:
            return "JWT"
        return "Unknown"
    def get_priority_modules(self, min_success_rate=30):
        """Vraća listu modula koji su najefikasniji"""
        stats = self.analyze()
        priority = []
        for typ, data in stats.items():
            if data["total"] == 0:
                continue
            rate = (data["hits"] / data["total"]) * 100
            if rate >= min_success_rate:
                priority.append(typ)
        return priority
