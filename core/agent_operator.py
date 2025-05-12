# core/agent_operator.py
import requests
from bs4 import BeautifulSoup

class AIOperater:
    def __init__(self, url):
        self.url = url
        self.rules = ["NO DDoS", "NO auth bypass", "Test only public endpoints"]

    def analyze(self):
        try:
            res = requests.get(self.url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            metadata = {
                "title": soup.title.string.strip() if soup.title else "N/A",
                "meta": self.extract_meta(soup),
                "links": [a.get("href") for a in soup.find_all("a") if a.get("href")]
            }
            return {"site_data": metadata, "allowed_actions": self.rules}
        except Exception as e:
            return {"error": str(e)}

    def extract_meta(self, soup):
        tag = soup.find("meta", attrs={"name": "description"})
        return tag["content"].strip() if tag and tag.get("content") else "N/A"
