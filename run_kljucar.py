from agents.ai_kljucar import AIKljucar

def run_ai_kljucar(site_data):
    kljucar = AIKljucar(site_data)
    selected_tools = kljucar.decide_tools()
    return selected_tools
