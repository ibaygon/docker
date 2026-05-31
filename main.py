from fastapi import FastAPI, HTTPException
import redis
import os
import json
from log_parser import parse_failed_ips
from inventory_manager import load_inventory, filter_vulnerable, group_by_department

app = FastAPI(title="Sys Admin Toolkit API", version="1.0.0")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

def get_redis():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True
    )

@app.get("/")
def status():
    return {"status": "ok", "service": "sys-admin-toolkit"}

@app.get("/health")
def health():
    try:
        r = get_redis()
        r.ping()
        redis_status = "ok"
    except Exception:
        redis_status = "unavailable"
    return {"api": "ok", "redis": redis_status}

@app.get("/logs/attackers")
def get_attackers():
    r = get_redis()
    cached = r.get("attackers")
    if cached:
        return {"source": "cache", "data": json.loads(cached)}
    failed_ips = parse_failed_ips("data/auth.log")
    result = [{"ip": ip, "attempts": count} for ip, count in
              sorted(failed_ips.items(), key=lambda x: x[1], reverse=True)]
    r.setex("attackers", 60, json.dumps(result))
    return {"source": "parsed", "data": result}

@app.post("/logs/suspicious/{ip}")
def report_suspicious(ip: str):
    r = get_redis()
    r.sadd("suspicious_ips", ip)
    return {"message": f"{ip} añadida a IPs sospechosas"}

@app.get("/logs/suspicious")
def list_suspicious():
    r = get_redis()
    ips = list(r.smembers("suspicious_ips"))
    return {"suspicious_ips": ips}

@app.get("/inventory")
def get_inventory():
    try:
        df = load_inventory("data/inventory.csv")
        vulnerable = filter_vulnerable(df)
        by_dept = group_by_department(vulnerable)
        return {
            "total": len(df),
            "vulnerable": len(vulnerable),
            "by_department": by_dept.to_dict(orient="records")
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="inventory.csv no encontrado")