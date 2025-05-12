import re
import sys

class InputValidator:
    def __init__(self, url):
        self.url = url

    def is_valid_url(self):
        pattern = re.compile(
            r'^https:\/\/hackerone\.com\/[a-zA-Z0-9_-]+\?type=team$'
        )
        return bool(pattern.match(self.url))

    def validate(self):
        if not self.is_valid_url():
            print("[ERROR] Uneti URL nije validan HackerOne team bounty link.")
            sys.exit(1)
        print("[OK] Validan HackerOne bounty link.")
        return True
