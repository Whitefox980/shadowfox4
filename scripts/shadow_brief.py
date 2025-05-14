import json
import os
from datetime import datetime
from fpdf import FPDF

def load_history():
    try:
        with open("data/mission_history.json") as f:
            missions = json.load(f)
        with open("data/fuzz_history.json") as f:
            fuzz = json.load(f)
    except:
        print("[BRIEF] Ne mogu da učitam podatke.")
        return [], {}
    return missions, fuzz

def classify(payload):
    if isinstance(payload, dict) and "role" in payload:
        return "JWT"
    p = str(payload).lower()
    if "script" in p or "alert" in p:
        return "XSS"
    if "' or" in p or '" or' in p:
        return "SQL Injection"
    if "127.0.0.1" in p or "internal" in p:
        return "SSRF"
    return "Unknown"

def generate_pdf(missions, fuzz):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"reports/ShadowBrief_{timestamp}.pdf"
    os.makedirs("reports", exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "ShadowFox - Komandni Izveštaj", ln=True, align="C")

    pdf.set_font("Arial", "B", 12)
    pdf.ln(10)
    pdf.cell(0, 10, "1. Misije i Mete:", ln=True)
    pdf.set_font("Arial", "", 11)
    for m in missions[-5:]:
        pdf.cell(0, 8, f"- {m.get('target')} ({m.get('timestamp')})", ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.ln(5)
    pdf.cell(0, 10, "2. Detektovani Tipovi Ranjivosti:", ln=True)
    pdf.set_font("Arial", "", 11)
    summary = {}
    for entries in fuzz.values():
        for e in entries:
            if not e.get("success"): continue
            typ = classify(e["payload"])
            summary[typ] = summary.get(typ, 0) + 1

    for typ, count in summary.items():
        pdf.cell(0, 8, f"- {typ}: {count} uspešnih payload-a", ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.ln(5)
    pdf.cell(0, 10, "3. AI Zaključak:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, "AI predlaže nastavak fokusiranih napada na visoko uspešne module uz evoluciju payload-a prema prethodnim mutacijama.")

    pdf.output(filename)
    print(f"[PDF] ShadowBrief sačuvan: {filename}")

if __name__ == "__main__":
    missions, fuzz = load_history()
    if missions and fuzz:
        generate_pdf(missions, fuzz)
