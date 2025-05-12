import dns.resolver

class SubdomainTakeoverFuzzer:
    def __init__(self):
        self.name = "Subdomain Takeover Fuzzer"
        self.subdomains = ["dev.", "test.", "stage.", "beta."]

    def run_tests(self, targets):
        results = {}
        for target in targets:
            for subdomain in self.subdomains:
                domain = f"{subdomain}{target}"
                response = self.check_dns(domain)
                results[domain] = response
        return results

    def check_dns(self, domain):
        try:
            answers = dns.resolver.resolve(domain, "A")
            return [str(rdata) for rdata in answers]
        except dns.resolver.NXDOMAIN:
            return "VULNERABLE: Subdomain does not exist"
        except dns.resolver.NoAnswer:
            return "SAFE"
