# agents/operator.py

def run_operator(target):
    print(f"[OPERATOR] Pokrećem obradu za metu: {target}")

    # Provera da li je dozvoljena
    forbidden_keywords = ["google", "facebook", "youtube", "gov", "mil"]
    if any(k in target.lower() for k in forbidden_keywords):
        print("[OPERATOR] Meta je van opsega ili zabranjena za testiranje.")
        return False

    print("[OPERATOR] Meta dozvoljena. Nastavljam sa analizom.")
    return True
