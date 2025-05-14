from fpdf import FPDF
from datetime import datetime
import os

def export_to_pdf(results, target_url):
    pdf = FPDF()
    pdf.add_page()

    # Samo regularni font — nema bold, nema stilova
    pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", "", 12)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pdf.cell(200, 10, txt=f"ShadowFox Izveštaj", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Meta: {target_url}", ln=True)
    pdf.cell(200, 10, txt=f"Vreme: {timestamp}", ln=True)
    pdf.ln(10)

    for module, data in results.items():
        pdf.set_font("DejaVu", "", 12)
        pdf.cell(200, 10, txt=f"[{module}]", ln=True)
        pdf.set_font("DejaVu", "", 11)

        if isinstance(data, str):
            pdf.multi_cell(0, 10, txt=data)
        elif isinstance(data, list):
            for payload in data:
                pdf.multi_cell(0, 8, txt=str(payload))
        elif isinstance(data, dict):
            for payload, res in data.items():
                pdf.multi_cell(0, 8, txt=f"{payload} --> {res}")
        pdf.ln(5)

    folder = "reports"
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"Report_{timestamp.replace(':','-')}.pdf")
    pdf.output(filename)
    print(f"[PDF] Izveštaj sačuvan: {filename}")
