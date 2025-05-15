import os
import subprocess

PDF_DIR = "data/pdf_reports"

def list_pdfs():
    return sorted(
        [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")],
        reverse=True
    )

def show_menu(pdfs):
    print("\n[PDF BROWSER] ShadowFox izveštaji:\n")
    for i, file in enumerate(pdfs):
        print(f"{i + 1}. {file}")

def open_pdf(file_path):
    print(f"[OPEN] Otvaram: {file_path}")
    subprocess.run(["termux-open", file_path])

def delete_pdf(file_path):
    os.remove(file_path)
    print(f"[DELETE] Obrisano: {file_path}")

def main():
    all_pdfs = list_pdfs()
    if not all_pdfs:
        print("Nema dostupnih PDF izveštaja.")
        return

    while True:
        print("\n=== SHADOWFOX MISSION CENTER ===")
        print("1. Prikaži sve")
        print("2. Prikaži poslednje 3")
        print("3. Filtriraj po vektoru (XSS, LFI, SQLi...)")
        print("4. Izlaz")
        choice = input("Izbor: ").strip()

        if choice == "1":
            selected = all_pdfs
        elif choice == "2":
            selected = all_pdfs[:3]
        elif choice == "3":
            keyword = input("Unesi vektor (npr. XSS): ").lower()
            selected = [f for f in all_pdfs if keyword in f.lower()]
            if not selected:
                print("[INFO] Nema PDF-ova za taj filter.")
                continue
        elif choice == "4":
            break
        else:
            print("[ERROR] Pogrešan izbor.")
            continue

        show_menu(selected)
        idx = input("\nIzaberi broj za otvaranje ili 'dN' za brisanje (npr. d2): ").strip()

        if idx.startswith("d") and idx[1:].isdigit():
            i = int(idx[1:]) - 1
            if 0 <= i < len(selected):
                delete_pdf(os.path.join(PDF_DIR, selected[i]))
            else:
                print("[ERROR] Pogrešan broj.")
        elif idx.isdigit():
            i = int(idx) - 1
            if 0 <= i < len(selected):
                open_pdf(os.path.join(PDF_DIR, selected[i]))
            else:
                print("[ERROR] Pogrešan broj.")
        else:
            print("[ERROR] Nevalidan unos.")

if __name__ == "__main__":
    main()
