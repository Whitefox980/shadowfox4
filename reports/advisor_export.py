import os
import json
from collections import Counter
from fpdf import FPDF
from datetime import datetime

MISSION_DIR = "data/mission_logs"
EXPORT_PATH = "data/pdf_reports/advisor_report.pdf"

RECOMMENDATIONS = {
    "XSS": "Koristi Content-Security-Policy (CSP) header i proper HTML escaping.",
    "SQL Injection": "Koristi parametrizovane upite (prepared statements).",
    "LFI": "Validiraj i filtriraj sve korisničke fajl putanje.",
    "SSRF": "Zabrani pristup internim IP-ima i koristi allow-list za URL-ove.",
    "BruteForce": "Ograniči broj pokušaja i koristi CAPTCHA sisteme.",
    "unknown": "Dodaj dodatnu AI analizu za nedefinisane vektore."
}

def load_vectors():
    counter = Counter()
    for file in os.listdir(MISSION_DIR):
        if not file.endswith(".json"):
            continue
        path = os.path.join(MISSION_DIR, file)
        try:
            with open(path, "r") as f:
                data = json.load(f)
            for r in data.get("results", []):
                if isinstance(r, dict):
                    vec = r.get("signature", {}).get("vector", "unknown")
                    counter[vec] += 1
        except:
            continue
    return counter

def export_pdf(vectors):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "WhiteShadowAdvisor - AI Preporuke Zastite", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, f"Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)

    for vec, count in vectors.most_common():
        advice = RECOMMENDATIONS.get(vec, "Nema konkretne preporuke.")
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"{vec} ({count}x):", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 10, advice)
        pdf.ln(3)

    os.makedirs("data/pdf_reports", exist_ok=True)
    pdf.output(EXPORT_PATH)
    print(f"[PDF] Izveštaj sačuvan u: {EXPORT_PATH}")

if __name__ == "__main__":
    data = load_vectors()
    export_pdf(data)
