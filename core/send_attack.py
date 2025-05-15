# core/send_attack.py
import urllib.parse
import requests

def send_attack(target, payload):
    try:
        encoded = urllib.parse.quote(payload, safe='')
        url = f"{target}?input={encoded}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*"
        }
        response = requests.get(url, headers=headers, timeout=5)
        print(f"[EXEC] Zahtev poslat: {url} | Status: {response.status_code}")
        return response.status_code, response.text
    except Exception as e:
        print(f"[ERROR] Napad nije uspeo: {e}")
        return None, ""
