from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import subprocess
import datetime
import os
import json
import time

from core.smart_shadow_agent import SmartShadowAgent
from scripts.shadow_brief import generate_pdf, load_history

app = FastAPI()

@app.post("/webhook/attack")
async def trigger_attack(request: Request):
    data = await request.json()
    target = data.get("target")

    if not target:
        return {"status": "error", "message": "No target provided."}

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[WEBHOOK] [{now}] Pokrećem AI napad na metu: {target}")

    try:
        agent = SmartShadowAgent()
        agent.run(target)
        return {"status": "ok", "message": f"Napad završen na: {target}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/webhook/report")
async def generate_report():
    try:
        missions, fuzz = load_history()
        generate_pdf(missions, fuzz)
        return {"status": "ok", "message": "PDF ShadowBrief generisan."}
    except Exception as e:
        return {"status": "error", "message": f"Greška: {str(e)}"}

@app.post("/webhook/full-mission")
async def full_mission(request: Request):
    data = await request.json()
    target = data.get("target")

    if not target:
        return {"status": "error", "message": "No target provided."}

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[WEBHOOK] [{now}] FULL MISSION na metu: {target}")

    try:
        agent = SmartShadowAgent()
        agent.run(target)
        time.sleep(1)
        missions, fuzz = load_history()
        generate_pdf(missions, fuzz)
        return JSONResponse({
            "status": "ok",
            "message": f"Full misija završena za: {target}",
            "pdf": "reports/ShadowBrief_*.pdf (pogledaj najnoviji)"
        })
    except Exception as e:
        return {"status": "error", "message": str(e)}
@app.get("/webhook/status")
async def get_status():
    try:
        with open("data/mission_history.json") as f:
            missions = json.load(f)
        with open("data/fuzz_history.json") as f:
            fuzz = json.load(f)
    except:
        return {"status": "error", "message": "Nema podataka."}

    if not missions:
        return {"status": "ok", "message": "Još uvek nije bilo misija."}

    last = missions[-1]
    target = last.get("target", "Nepoznata")
    timestamp = last.get("timestamp", "Nepoznat")
    results = last.get("results", {})
    total = sum([1 for r in results.values()])
    types = list(results.keys())

    return {
        "status": "ok",
        "last_target": target,
        "timestamp": timestamp,
        "detektovani_moduli": types,
        "broj_payloada": total
    }
