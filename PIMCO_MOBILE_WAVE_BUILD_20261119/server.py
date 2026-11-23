from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
from datetime import datetime, timezone
import sqlite3, os, re, hmac

BASE = Path(__file__).resolve().parent
DB = BASE / "deposits.db"
app = Flask(__name__, static_folder="static", static_url_path="/static")

def connect():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with connect() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS deposits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount INTEGER NOT NULL,
        reference TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'PENDING',
        created_at TEXT NOT NULL)
        """)

init_db()

@app.get("/")
def home():
    return send_from_directory(BASE, "index.html")

@app.post("/api/deposits")
def create_deposit():
    data = request.get_json(silent=True) or {}
    try:
        amount = int(data.get("amount", 0))
    except (ValueError, TypeError):
        return jsonify(error="Invalid deposit amount."), 400
    reference = str(data.get("reference", "")).strip()
    if amount <= 0 or amount > 1000000000:
        return jsonify(error="Enter a valid deposit amount."), 400
    if not reference or len(reference) > 80 or not re.fullmatch(r"[A-Za-z0-9 _./-]+", reference):
        return jsonify(error="Enter a valid transaction reference."), 400
    with connect() as db:
        cur = db.execute(
        "INSERT INTO deposits(amount,reference,status,created_at) VALUES(?,?,?,?)",
        (amount,reference,"PENDING",datetime.now(timezone.utc).isoformat()))
        deposit_id = cur.lastrowid
    return jsonify(id=deposit_id,status="PENDING"), 201

@app.get("/api/admin/deposits")
def admin_deposits():
    token = os.environ.get("ADMIN_TOKEN", "")
    supplied = request.headers.get("X-Admin-Token", "")
    if not token or not hmac.compare_digest(supplied, token):
        return jsonify(error="Unauthorized"), 401
    with connect() as db:
        rows = db.execute("SELECT id,amount,reference,status,created_at FROM deposits ORDER BY id DESC").fetchall()
    return jsonify(deposits=[dict(row) for row in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",8000)))
