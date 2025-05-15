# agents/recon_agent.py

import socket
from urllib.parse import urlparse

def analyze_target(url):
    print("[RECON] Analiziram metu...")

    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        ip = socket.gethostbyname(domain)
    except Exception as e:
        print(f"[RECON] Ne mogu da resolve-ujem IP: {e}")
        ip = "Nepoznata"

    platform = "custom"
    if any(x in url for x in ["wp-", "wordpress"]):
        platform = "WordPress"
    elif any(x in url for x in ["shopify", "cart"]):
        platform = "Shop"
    elif any(x in url for x in ["admin", "login"]):
        platform = "LoginPanel"

    print(f"[RECON] Detektovan tip mete: web | Platforma: {platform}")
    return {
        "ip": ip,
        "domain": domain,
        "platform": platform
    }
