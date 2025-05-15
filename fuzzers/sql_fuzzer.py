class SQLiFuzzer:
    def fuzz_target(self, target):
        payloads = [
            "' OR 1=1 --",
            "'; DROP TABLE users; --",
            "\" OR \"\" = \""
        ]
        results = []
        for p in payloads:
            success = "1=1" in p or "DROP" in p
            results.append({"payload": p, "success": success})
        return results
