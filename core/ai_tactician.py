import json
from collections import Counter

class AITactician:
    def __init__(self, scan_path="data/scan_results.json"):
        with open(scan_path) as f:
            self.data = json.load(f)
        self.recommendations = {}

    def analyze(self):
        all_hits = []
        for mod, result in self.data.items():
            for entry, verdict in result.items():
                if "VULNERABLE" in verdict:
                    all_hits.append(mod)

        counter = Counter(all_hits)
        total = sum(counter.values())

        self.recommendations["top_modules"] = counter.most_common(5)
        self.recommendations["strategy"] = self.generate_strategy(counter, total)

    def generate_strategy(self, counter, total):
        if not total:
            return "Nijedna ranjivost nije pronađena, sledeći put koristi recon module i AI evaluaciju meta."
        
        primary = counter.most_common(1)[0][0]
        return f"Fokusiraj se na '{primary}' jer se pokazao kao najuspešniji vektor. Predlaže se rana upotreba tog modula i mutacija payload-a u sledećem ciklusu."

    def export(self, path="data/tactics.json"):
        with open(path, "w") as f:
            json.dump(self.recommendations, f, indent=2)
        print("[TACTICIAN] Taktika sačuvana u", path)

# Primer poziva
if __name__ == "__main__":
    tact = AITactician()
    tact.analyze()
    tact.export()
