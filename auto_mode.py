from core.smart_shadow_agent import SmartShadowAgent
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python auto_mode.py <target_url>")
        return

    target_url = sys.argv[1]
    agent = SmartShadowAgent()
    agent.run(target_url)

if __name__ == "__main__":
    main()
