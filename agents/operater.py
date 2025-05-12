import requests
from bs4 import BeautifulSoup
from core.shadow_core_log import log

class AIOperater:
    def __init__(self, url):
        self.url = url
        self.rules = ["no DDoS", "no auth bypass", "respect scope"]

    def analyze(self):
        try:
            response = requests.get(self.url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            metadata = {
                "title": soup.title.string.strip() if soup.title else "N/A",
                "meta": self.extract_meta(soup),
                "links": list({a.get("href") for a in soup.find_all("a") if a.get("href") and a.get("href").startswith("http")}),
                "rules": self.rules
            }

            log("Operater", f"Analizirana meta: {metadata['title']}")
            return metadata

        except Exception as e:
            log("Operater", f"Greška pri analizi: {e}", status="error")
            return {}

    def extract_meta(self, soup):
        meta_tag = soup.find("meta", attrs={"name": "description"})
        return meta_tag["content"].strip() if meta_tag else "N/A"
