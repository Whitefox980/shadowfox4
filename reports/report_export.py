import os
import json
from fpdf import FPDF
from datetime import datetime

MISSION_FOLDER = "data/mission_logs"
EXPORT_FOLDER = "data/pdf_reports"
os.makedirs(EXPORT_FOLDER, exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "ShadowFox Misija", 0, 1, "C")

    def mission_block(self, mission_data):
        self.set_font("Arial", "", 10)
        self.cell(0, 10, f"Meta: {mission_data['target']}", 0, 1)
        self.cell(0, 10, f"Vreme: {mission_data['timestamp']}", 0, 1)
        self.ln(2)

        for r in mission_data["results"]:
            if not isinstance(r, dict):
                print(f"[WARN] Preskačem nevalidan rezultat: {r}")
                continue
            p = r["payload"]
            s = r["success"]
            v = r["signature"]["vector"]
            risk = assess_risk(p)
            self.multi_cell(0, 7, f"[{v}] {'[OK]' if s else '[X]'} {p} → Rizik: {risk}", border=0)
        self.ln(5)
def assess_risk(payload):
    payload = payload.lower()
    if any(x in payload for x in ["<script>", "onerror", "svg", "alert"]):
        return "Visok (XSS)"
    elif any(x in payload for x in ["127.0.0.1", "localhost", "169.254"]):
        return "Kritičan (SSRF)"
    elif "etc/passwd" in payload or "boot.ini" in payload:
        return "Visok (LFI)"
    elif any(x in payload for x in ["or 1=1", "drop table", '" OR "" =']):
        return "Srednji (SQLi)"
    else:
        return "Nizak"

def generate_reports():
    for file in os.listdir(MISSION_FOLDER):
        if file.endswith(".json"):
            path = os.path.join(MISSION_FOLDER, file)
            with open(path, "r") as f:
                data = json.load(f)

            pdf = PDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.mission_block(data)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_name = f"{EXPORT_FOLDER}/{file.replace('.json', '')}_{timestamp}.pdf"
            pdf.output(pdf_name)
            print(f"[PDF] Exportovano: {pdf_name}")

if __name__ == "__main__":
    generate_reports()
