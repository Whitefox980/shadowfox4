import sys
from core.shadow_recon import ShadowRecon
from core.kljucar import Kljucar
from core.smart_shadow_agent import SmartShadowAgent

def main():
    if len(sys.argv) != 2:
        print("Usage: python shadow_control.py <meta_url>")
        return

    target = sys.argv[1]
    print(f"[OPERATOR] Pokrećem obradu za metu: {target}")

    # 1. Recon analiza
    scope = ShadowRecon(target)
    scope_info = scope.analyze_scope()

    if not scope_info["allowed"]:
        print("[OPERATOR] Meta je van opsega ili zabranjena za testiranje.")
        return

    print(f"[RECON] Detektovan tip mete: {scope_info['type']} | Platforma: {scope_info['platform']}")

    # 2. Kljucar bira dozvoljene module
    kljucar = Kljucar()
    plan = kljucar.generate_plan(scope_info)
    print(f"[KLJUČAR] Planirani moduli: {plan['modules']}")

    # 3. ShadowAgent izvršava
    agent = SmartShadowAgent()
    agent.run(target, plan["modules"])

if __name__ == "__main__":
    main()
