# agents/ai_brain.py

def suggest_vectors(recon_data):
    platform = recon_data.get("platform", "").lower()
    vectors = []

    if platform == "wordpress":
        vectors = ["XSS", "LFI", "SQL Injection"]
    elif platform == "shop":
        vectors = ["SQL Injection", "XSS"]
    elif platform == "loginpanel":
        vectors = ["SQL Injection", "BruteForce"]
    else:
        vectors = ["XSS", "SQL Injection", "LFI", "SSRF"]

    print(f"[AI BRAIN] Strateg preporučuje: {vectors}")
    return vectors
