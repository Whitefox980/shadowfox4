import json
from fpdf import FPDF
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "ShadowFox - Izveštaj Skeniranja", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Strana {self.page_no()}", align="C")

    def add_section(self, title, items, color=(0,0,0)):
        self.set_font("Arial", "B", 12)
        self.set_text_color(*color)
        self.cell(0, 10, title, ln=True)
        self.set_font("Arial", "", 11)
        self.set_text_color(0, 0, 0)
        for mod, url in items:
            self.multi_cell(0, 8, f"- {mod} @ {url}")

    def add_tools_summary(self, tools):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Statistika alata", ln=True)
        self.set_font("Arial", "", 11)
        for tool, count in tools.items():
            self.cell(0, 8, f"• {tool}: {count} pogodaka", ln=True)

def generate_pdf(summary_path="data/summary.json", output="data/report.pdf"):
    with open(summary_path) as f:
        summary = json.load(f)

    pdf = PDFReport()
    pdf.add_page()

    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 8, f"Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    pdf.ln(5)
    pdf.add_section("Otkrivene ranjivosti", summary.get("vulnerable", []), color=(255,0,0))
    pdf.ln(5)
    pdf.add_section("Greške tokom testiranja", summary.get("errors", []), color=(255,165,0))
    pdf.ln(5)
    pdf.add_section("Sigurni moduli", summary.get("safe", []), color=(0,128,0))
    pdf.ln(5)
    pdf.add_tools_summary(summary.get("tools", {}))

    pdf.output(output)
    print("[PDF] Izveštaj sačuvan u", output)

if __name__ == "__main__":
    generate_pdf()
