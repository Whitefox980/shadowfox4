import markdown
from weasyprint import HTML

with open("data/mission_log.md", "r") as f:
    md_text = f.read()

html = markdown.markdown(md_text)

HTML(string=html).write_pdf("data/mission_log.pdf")

print("[PDF] Generisan 'data/mission_log.pdf'")
