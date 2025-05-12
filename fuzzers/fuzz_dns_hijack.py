import dns.resolver

class DNSHijackFuzzer:
    def __init__(self):
        self.name = "DNS Hijacking Fuzzer"
        self.records = ["A", "MX", "CNAME", "TXT", "NS"]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            results[target] = self.check_dns(target)
        return results

    def check_dns(self, domain):
        result = {}
        for record in self.records:
            try:
                answers = dns.resolver.resolve(domain, record, lifetime=3)
                result[record] = [str(rdata) for rdata in answers]
            except dns.resolver.NoAnswer:
                result[record] = "No record found"
            except dns.resolver.NXDOMAIN:
                result[record] = "Domain does not exist"
            except Exception as e:
                result[record] = f"Error: {str(e)}"
        return result
