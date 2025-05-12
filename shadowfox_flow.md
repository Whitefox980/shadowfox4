# ShadowFox Agentni Protokol (v1.0)

## ✅ Osnovni Princip:
Unos = **jedan jedini URL** (HackerOne/Bugcrowd bounty stranica).  
Sve ostalo rade autonomni AI agenti, svaki za sebe.

---

## 🧠 STRUKTURA AGENATA

### 1. AI Operater (`ai_operater_h1.py`)
- ZADATAK:
  - Parsira bounty stranicu
  - Koristi `recon_tavily.py` ako treba dodatna pretraga
  - Analizira meta tagove, scope, pravila
  - Kreira fajl `op_meta.json`:
    ```json
    {
      "team": "Zooplus",
      "reward": "Yes",
      "rules": ["no ddos", "no phishing"],
      "domains": ["shop.zooplus.com", "api.zooplus.com"],
      "auth_required": true,
      "login_url": "https://shop.zooplus.com/login",
      "discovered_links": [...]
    }
    ```

---

### 2. Shadow Agent (`ai_shadow_agent.py`)
- ZADATAK:
  - Uzima `op_meta.json`
  - Radi osnovni `recon_engine.py`: DNS lookup, HTTP check
  - Identifikuje tip mete: API, frontend, auth zone, CDN...
  - Određuje vektore napada → `vectors.json`
    ```json
    {
      "SQLi": true,
      "XSS": true,
      "LFI": false,
      "JWT": true
    }
    ```
  - Šalje vektore Ključaru

---

### 3. Ključar (`ai_kljucar.py`)
- ZADATAK:
  - Prima `vectors.json`
  - Bira konkretne fuzzy module iz `/modules`
  - Generiše `attack_plan.json`:
    ```json
    {
      "modules": [
        "fuzz_sql", "fuzz_xss", "fuzz_jwt"
      ],
      "severity_expectation": "medium-high"
    }
    ```

---

### 4. Strateg (`ai_strateg.py`)
- ZADATAK:
  - Uzima `attack_plan.json`
  - Izvršava sve navedene fuzz module
  - Prikuplja rezultate
  - Analizira uspešnost
  - Kreira `strategic_report.json`
  - Ažurira `mutation_history.json` ako je neki napad uspešan
  - Ako je napad uspešan:
    - generiše mutaciju u `mutated_attacks/`
    - dodaje tagove: `effective`, `reflected`, `zero-day`

---

## 🔁 Tok rada sistema

1. Korisnik unosi bounty link → `ai_operater_h1.py`
2. Operater pravi `op_meta.json`
3. Shadow Agent generiše `vectors.json`
4. Ključar pravi `attack_plan.json`
5. Strateg izvršava i pravi `strategic_report.json`

---

## 📁 Standardni Folderi
