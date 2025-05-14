import os

LOG_PATH = "data/operator_log.txt"

def show():
    if not os.path.exists(LOG_PATH):
        print("[LOG] Nema zabeleženih aktivnosti.")
        return
    with open(LOG_PATH) as f:
        lines = f.readlines()[-10:]
        print("\n[OPERATOR LOG - POSLEDNJIH 10 LINIJA]\n")
        for line in lines:
            print(f" - {line.strip()}")

if __name__ == "__main__":
    show()
