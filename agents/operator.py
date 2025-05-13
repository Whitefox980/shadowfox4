class Operater:
    def __init__(self, target_url):
        self.url = target_url

    def analyze(self):
        print(f"[OPERATER] [INFO] Analizirana meta: {self.url.split('//')[-1].split('?')[0].capitalize()}")
        return {
            "site_data": {
                "url": self.url,
                "platform": "generic",
                "headers": {
                    "server": "unknown"
                }
            }
        }
