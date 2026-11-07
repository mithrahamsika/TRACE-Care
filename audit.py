
import sqlite3
from pathlib import Path
from datetime import datetime

DATABASE_NAME = Path(__file__).resolve().parent / "tracecare.db"


def create_audit_table():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            case_id INTEGER,
            event_type TEXT NOT NULL,
            event_details TEXT NOT NULL,
            performed_by TEXT,
            event_time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def log_event(patient_id, event_type, event_details,
              case_id=None, performed_by="System"):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO audit_logs (
            patient_id, case_id, event_type,
            event_details, performed_by, event_time
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        patient_id,
        case_id,
        event_type,
        event_details,
        performed_by,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_audit_logs(patient_id=None):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    if patient_id:
        cursor.execute("""
            SELECT * FROM audit_logs
            WHERE patient_id = ?
            ORDER BY id DESC
        """, (patient_id,))
    else:
        cursor.execute("""
            SELECT * FROM audit_logs
            ORDER BY id DESC
        """)

    logs = cursor.fetchall()
    conn.close()

    return logs


create_audit_table()
