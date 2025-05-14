import json
import os
from fpdf import FPDF
from datetime import datetime

def load_history(path="data/fuzz_history.json"):
    if not os.path.exists(path):
        print("[PDF] Nema fuzz istorije.")
        return {}
    with open(path) as f:
        return json.load(f)

def export_to_pdf(data):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"reports/FuzzReport_{timestamp}.pdf"
    os.makedirs("reports", exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "AI Fuzz Evolucija - ShadowFox Izveštaj", ln=True, align="C")

    for typ, payloads in data.items():
        pdf.set_font("Arial", "B", 12)
        pdf.ln(10)
        pdf.cell(0, 10, f"[{typ.upper()}] ({len(payloads)} pokušaja)", ln=True)
        pdf.set_font("Arial", "", 11)
        for entry in payloads:
            status = "✔️" if entry.get("success") else "✖️"
            line = f"{status} {entry.get('payload')}"
            pdf.multi_cell(0, 8, line)

    pdf.output(filename)
    print(f"[PDF] Sačuvan kao: {filename}")

if __name__ == "__main__":
    history = load_history()
    if history:
        export_to_pdf(history)
