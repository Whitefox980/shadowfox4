class SSRFFuzzer:
    def fuzz_target(self, target):
        payloads = [
            "http://127.0.0.1:80",
            "http://localhost/admin",
            "http://169.254.169.254/latest/meta-data/"
        ]
        results = []
        for p in payloads:
            success = "127.0.0.1" in p or "169.254" in p
            results.append({"payload": p, "success": success})
        return results
