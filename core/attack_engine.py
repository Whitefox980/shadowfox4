# core/attack_engine.py

import urllib.request

def send_attack(target, payload):
    try:
        url = f"{target}?input={payload}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*"
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            print(f"[EXEC] Poslat: {url} | Status: {response.status}")
            return response.status, response.read().decode()
    except Exception as e:
        print(f"[ERROR] Napad nije uspeo: {e}")
        return None, ""
