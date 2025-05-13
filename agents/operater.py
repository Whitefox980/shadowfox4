import requests
from bs4 import BeautifulSoup
from utils.logger import log_info, log_error

class AIOperater:
    def __init__(self, url):
        self.url = url

    def analyze(self):
        try:
            response = requests.get(self.url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string.strip() if soup.title else "Unknown"
            meta_tag = soup.find("meta", attrs={"name": "description"})
            meta = meta_tag["content"].strip() if meta_tag else "N/A"
            links = [link.get("href") for link in soup.find_all("a") if link.get("href")]

            site_data = {
                "title": title,
                "meta_description": meta,
                "links": links[:10]
            }

            log_info(f"Analizirana meta: {title}")
            return {"site_data": site_data}

        except Exception as e:
            log_error(f"Greška pri analizi: {e}")
            return {"site_data": {
                "title": "Unknown",
                "meta_description": "N/A",
                "links": []
            }}

    def extract_meta(self, soup):
        meta_tag = soup.find("meta", attrs={"name": "description"})
        return meta_tag["content"].strip() if meta_tag else "N/A"
