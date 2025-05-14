import zipfile, os

def export():
    files = [
        "data/fuzz_history.json",
        "data/mission_history.json",
        "reports/"
    ]
    with zipfile.ZipFile("ShadowFox_Export.zip", "w") as z:
        for path in files:
            if os.path.isdir(path):
                for f in os.listdir(path):
                    z.write(os.path.join(path, f))
            elif os.path.exists(path):
                z.write(path)
    print("[EXPORT] ShadowFox_Export.zip spreman.")

if __name__ == "__main__":
    export()
