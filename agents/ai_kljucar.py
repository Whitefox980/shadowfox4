import json

class AIKljucar:
    def __init__(self, site_data):
        self.site_data = site_data
        self.rules = {
            "sql": ["?id=", "select", "search"],
            "xss": ["<script>", "input", "comment"],
            "rfi": ["file=", "url="],
            "cmd": ["cmd=", "exec"],
            "redirect": ["redirect=", "next="],
            "jwt": ["Authorization", "token"],
            "ldap": ["directory", "user=admin"]
        }
        self.mapping = {
            "sql": "fuzz_sql",
            "xss": "fuzz_xss",
            "rfi": "fuzz_rfi",
            "cmd": "fuzz_cmd",
            "redirect": "fuzz_redirect",
            "jwt": "fuzz_jwt",
            "ldap": "fuzz_ldap"
        }

    def decide_tools(self):
        used = set()
        content = json.dumps(self.site_data).lower()
        for keyword_group, module in self.mapping.items():
            for hint in self.rules[keyword_group]:
                if hint in content:
                    used.add(module)
        return list(used)
