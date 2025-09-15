# db.py
import sqlite3
import datetime
import json
from typing import List, Dict, Any

DB_FILE = "ai_health.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        symptoms TEXT,
        advice TEXT,
        probable_conditions TEXT,
        severity TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_query(symptoms: str, result: Dict[str, Any]) -> None:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO queries (timestamp, symptoms, advice, probable_conditions, severity) VALUES (?, ?, ?, ?, ?)",
        (datetime.datetime.utcnow().isoformat(), symptoms, result.get("advice", ""), json.dumps(result.get("probable_conditions", [])), result.get("severity", "unknown"))
    )
    conn.commit()
    conn.close()

def get_history(limit: int = 20) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, symptoms, advice, probable_conditions, severity FROM queries ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    out = []
    for r in rows:
        out.append({
            "id": r[0],
            "timestamp": r[1],
            "symptoms": r[2],
            "advice": r[3],
            "probable_conditions": json.loads(r[4]) if r[4] else [],
            "severity": r[5]
        })
    return out
