class Kljucar:
    def generate_plan(self, scope_info):
        platform = scope_info.get("platform", "")
        attack_type = scope_info.get("type", "web")

        modules = []

        if attack_type == "web":
            modules.extend(["XSS", "SQL Injection", "LFI"])
        if platform == "custom":
            modules.append("SSRF")
        if "wordpress" in platform.lower():
            modules.append("Brute Force")

        return {
            "modules": list(set(modules))  # bez duplikata
        }
