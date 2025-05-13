import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from core.memory import MissionMemory

def export_to_pdf(index):
    memory = MissionMemory()
    history = memory.get_all_missions()

    if index < 0 or index >= len(history):
        print("[ERROR] Neispravan broj misije.")
        return

    entry = history[::-1][index]  # Uzima poslednje (ili n-to poslednje) unazad
    timestamp = entry.get("timestamp", "Nepoznat datum")
    results = entry.get("results", {})
    target = entry.get("target", "Nepoznata meta")

    pdf_file = f"data/missions/mission_{timestamp.replace(':', '-')}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4
    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, f"ShadowFox Misija: {target}")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(40, y, f"Datum: {timestamp}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "REZULTATI:")
    y -= 20

    for mod, res in results.items():
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, f"[{mod}]")
        y -= 15
        c.setFont("Helvetica", 10)
        lines = str(res).split("\n")
        for line in lines:
            c.drawString(60, y, line[:100])
            y -= 12
            if y < 50:
                c.showPage()
                y = height - 40

    c.save()
    print(f"[PDF] Izveštaj sačuvan kao: {pdf_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: python scripts/export_pdf.py <broj_misije>")
    else:
        export_to_pdf(int(sys.argv[1]))
