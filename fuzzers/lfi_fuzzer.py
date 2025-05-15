class LFIFuzzer:
    def fuzz_target(self, target):
        payloads = [
            "../../etc/passwd",
            "..\\..\\..\\boot.ini",
            "../../../../windows/win.ini"
        ]
        results = []
        for p in payloads:
            success = "/etc/passwd" in p or "boot.ini" in p
            results.append({"payload": p, "success": success})
        return results
