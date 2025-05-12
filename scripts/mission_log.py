import json
from datetime import datetime

def load_scan_results():
    with open("data/scan_results.json") as f:
        return json.load(f)

def create_log(results, url):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# SHADOWFOX MISIJA",
        f"**Meta:** {url}",
        f"**Datum:** {now}",
        "\n---\n",
        "## Detalji napada\n"
    ]

    for module, outcome in results.items():
        lines.append(f"### {module}")
        if isinstance(outcome, dict):
            for target, verdict in outcome.items():
                lines.append(f"- **{target}** → `{verdict}`")
        else:
            lines.append(f"- Rezultat: `{outcome}`")
        lines.append("")

    # Zaključak
    vuln_found = sum(1 for m in results.values() if "VULNERABLE" in str(m))
    lines.append("---\n")
    lines.append(f"**Ukupno pronađenih ranjivosti:** `{vuln_found}`\n")
    lines.append("**Preporuka:** Pokrenuti dodatnu analizu i pripremiti AI patch modul.\n")

    return "\n".join(lines)

if __name__ == "__main__":
    with open("data/scan_results.json") as f:
        meta_url = list(json.load(f).values())[0]
        if isinstance(meta_url, dict):
            meta_url = list(meta_url.keys())[0]

    results = load_scan_results()
    log_md = create_log(results, meta_url)

    with open("data/mission_log.md", "w") as f:
        f.write(log_md)

    print("[LOG] Generisan 'data/mission_log.md'")
