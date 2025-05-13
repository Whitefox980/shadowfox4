import time
import random

def random_delay(min_delay=0.4, max_delay=1.7):
    """Simulira korisnički interval između zahteva."""
    time.sleep(random.uniform(min_delay, max_delay))

def fake_headers():
    """Generiše lažne zaglavlja da izgledamo kao pravi korisnik."""
    return {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (Linux; Android 10)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X)"
        ]),
        "Referer": "https://google.com",
        "Accept-Language": "en-US,en;q=0.9"
    }

