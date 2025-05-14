import os
import sys
from core.signature_validator import SignatureValidator

if len(sys.argv) != 5:
    print("Usage:")
    print("  python scripts/verify_signature.py <payload> <timestamp> <vector> <signature>")
    sys.exit(1)

payload = sys.argv[1]
timestamp = sys.argv[2]
vector = sys.argv[3]
signature = sys.argv[4]

validator = SignatureValidator()
if validator.validate(payload, timestamp, vector, signature):
    print("[OK] Signature is VALID.")
else:
    print("[FAIL] Signature is INVALID.")
def verify():
    path = "data/signatures/"
    sigs = sorted(os.listdir(path))[-10:]

    print("\n[SHADOW SIGNATURE VERIFY - Last 10]\n")
    for sig in sigs:
        with open(os.path.join(path, sig)) as f:
            content = f.read()
        print(f"{sig}")
        print("-" * 40)
        print(content)
        print()

if __name__ == "__main__":
    verify()
