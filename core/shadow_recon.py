class ShadowRecon:
    def __init__(self, target):
        self.target = target

    def analyze_scope(self):
        if "zooplus" in self.target:
            return {
                "allowed": True,
                "type": "web",
                "platform": "custom",
                "domain": "zooplus.com"
            }
        return {
            "allowed": False
        }
