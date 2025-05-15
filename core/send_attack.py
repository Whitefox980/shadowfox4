import requests

def send_attack(target, payload):
    try:
        url = f"{target}?input={payload}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html"
        }
        response = requests.get(url, headers=headers, timeout=5)
        print(f"[EXEC] Zahtev poslat: {url}")
        return response.status_code, response.text
    except Exception as e:
        print(f"[ERROR] Napad nije uspeo: {e}")
        return None, ""
