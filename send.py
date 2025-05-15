print("[DEBUG] Koristim PRAVI send_attack.py")
# test_send.py
from core.send_attack import send_attack
send_attack("https://example.com", "' OR 1=1 --")
from core.send_attack import send_attack
send_attack("https://example.com", "' OR 1=1 --")
import traceback

def send_attack(target, payload):
    print("[DEBUG] === UŠAO U PRAVI send_attack ===")
    traceback.print_stack()
    ...
