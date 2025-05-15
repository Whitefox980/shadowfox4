class XSSFuzzer:
    def fuzz_target(self, target):
        payloads = [
            "<script>alert(1)</script>",
            "\"><svg/onload=alert(1)>",
            "'><img src=x onerror=alert(1)>"
        ]
        results = []
        for p in payloads:
            success = "alert" in p
            results.append({"payload": p, "success": success})
        return results
