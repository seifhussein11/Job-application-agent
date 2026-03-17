import sqlite3
import json
from datetime import datetime

DB_PATH = "applications.db"

def init_db():
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""  CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            company_name TEXT,
            job_title TEXT,
            raw_score REAL,
            tailored_score REAL,
            tailored_cv TEXT,
            cover_letter TEXT,
            judge_feedback TEXT
        )
          """)
    
    conn.commit()
    conn.close()
    
    
def save_application(state):
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO applications (
            created_at, company_name, job_title,
            raw_score, tailored_score,tailored_cv, 
            cover_letter, judge_feedback
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        state.get("company_name", ""),
        state.get("job_title", ""),
        state.get("raw_match_score", 0.0),
        state.get("tailored_match_score", 0.0),
        state.get("tailored_cv", ""),
        state.get("cover_letter", ""),
        state.get("judge_feedback", ""),
    ))
    conn.commit()
    conn.close()
    
    
def get_all_applications():
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM applications ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]