
import sqlite3
from pathlib import Path
from datetime import datetime
from audit import log_event

DATABASE_NAME = Path(__file__).resolve().parent / "tracecare.db"


def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT UNIQUE NOT NULL,
            patient_name TEXT NOT NULL,
            screening_type TEXT NOT NULL,
            screening_date TEXT NOT NULL,
            contact TEXT,
            follow_up_status TEXT NOT NULL,
            follow_up_date TEXT,
            outcome_notes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS barriers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            barrier TEXT NOT NULL,
            description TEXT,
            barrier_status TEXT NOT NULL,
            recommended_action TEXT,
            recommendation_reason TEXT,
            approval_status TEXT DEFAULT 'Pending',
            assigned_to TEXT,
            action_status TEXT DEFAULT 'Not Started',
            assigned_date TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
        )
    """)

    # Migrate existing patient table
    cursor.execute("PRAGMA table_info(patients)")
    patient_columns = [column[1] for column in cursor.fetchall()]

    patient_new_columns = {
        "follow_up_date": "TEXT",
        "outcome_notes": "TEXT"
    }

    for column, definition in patient_new_columns.items():
        if column not in patient_columns:
            cursor.execute(
                f"ALTER TABLE patients ADD COLUMN {column} {definition}"
            )

    # Migrate existing barrier table
    cursor.execute("PRAGMA table_info(barriers)")
    barrier_columns = [column[1] for column in cursor.fetchall()]

    barrier_new_columns = {
        "recommended_action": "TEXT",
        "recommendation_reason": "TEXT",
        "approval_status": "TEXT DEFAULT 'Pending'",
        "assigned_to": "TEXT",
        "action_status": "TEXT DEFAULT 'Not Started'",
        "assigned_date": "TEXT"
    }

    for column, definition in barrier_new_columns.items():
        if column not in barrier_columns:
            cursor.execute(
                f"ALTER TABLE barriers ADD COLUMN {column} {definition}"
            )

    conn.commit()
    conn.close()


def add_patient(patient_id, patient_name, screening_type,
                screening_date, contact, follow_up_status):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO patients (
                patient_id, patient_name, screening_type,
                screening_date, contact, follow_up_status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            patient_id, patient_name, screening_type,
            screening_date, contact, follow_up_status
        ))

        conn.commit()
        conn.close()

        log_event(
            patient_id,
            "Patient Registration",
            f"Patient registered for {screening_type}",
            performed_by="System"
        )

        return True

    except sqlite3.IntegrityError:
        conn.close()
        return False


def get_all_patients():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients ORDER BY id DESC")
    patients = cursor.fetchall()

    conn.close()
    return patients


def add_barrier(patient_id, barrier, description,
                barrier_status, recommended_action,
                recommendation_reason):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO barriers (
            patient_id, barrier, description, barrier_status,
            recommended_action, recommendation_reason,
            approval_status, action_status
        )
        VALUES (?, ?, ?, ?, ?, ?, 'Pending', 'Not Started')
    """, (
        patient_id, barrier, description, barrier_status,
        recommended_action, recommendation_reason
    ))

    barrier_id = cursor.lastrowid

    conn.commit()
    conn.close()

    log_event(
        patient_id,
        "Barrier Identification",
        f"Barrier identified: {barrier}",
        case_id=barrier_id
    )


def get_all_barriers():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM barriers ORDER BY id DESC")
    barriers = cursor.fetchall()

    conn.close()
    return barriers


def update_approval(barrier_id, decision):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT patient_id, barrier
        FROM barriers
        WHERE id = ?
    """, (barrier_id,))

    record = cursor.fetchone()

    cursor.execute("""
        UPDATE barriers
        SET approval_status = ?
        WHERE id = ?
    """, (decision, barrier_id))

    conn.commit()
    conn.close()

    if record:
        patient_id, barrier = record

        log_event(
            patient_id,
            "Recommendation Approval",
            f"{barrier} recommendation was {decision.lower()}",
            case_id=barrier_id,
            performed_by="Healthcare Staff"
        )


def get_approved_barriers():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM barriers
        WHERE approval_status = 'Approve'
        ORDER BY id DESC
    """)

    barriers = cursor.fetchall()
    conn.close()

    return barriers


def assign_case(barrier_id, staff_name):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT patient_id, barrier
        FROM barriers
        WHERE id = ? AND approval_status = 'Approve'
    """, (barrier_id,))

    record = cursor.fetchone()

    cursor.execute("""
        UPDATE barriers
        SET assigned_to = ?, assigned_date = ?
        WHERE id = ? AND approval_status = 'Approve'
    """, (
        staff_name,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        barrier_id
    ))

    updated = cursor.rowcount

    conn.commit()
    conn.close()

    if updated > 0 and record:
        patient_id, barrier = record

        log_event(
            patient_id,
            "Staff Assignment",
            f"{barrier} case assigned to {staff_name}",
            case_id=barrier_id,
            performed_by="Healthcare Staff"
        )


def update_action_status(barrier_id, status):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT patient_id, barrier
        FROM barriers
        WHERE id = ? AND approval_status = 'Approve'
    """, (barrier_id,))

    record = cursor.fetchone()

    cursor.execute("""
        UPDATE barriers
        SET action_status = ?
        WHERE id = ? AND approval_status = 'Approve'
    """, (status, barrier_id))

    updated = cursor.rowcount

    conn.commit()
    conn.close()

    if updated > 0 and record:
        patient_id, barrier = record

        log_event(
            patient_id,
            "Intervention Progress",
            f"{barrier} intervention status updated to {status}",
            case_id=barrier_id,
            performed_by="Healthcare Staff"
        )


def update_patient_followup(patient_id, follow_up_status,
                            follow_up_date, outcome_notes):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patients
        SET follow_up_status = ?,
            follow_up_date = ?,
            outcome_notes = ?
        WHERE patient_id = ?
    """, (
        follow_up_status,
        follow_up_date,
        outcome_notes,
        patient_id
    ))

    updated = cursor.rowcount

    conn.commit()
    conn.close()

    if updated > 0:
        log_event(
            patient_id,
            "Patient Follow-up",
            f"Follow-up status updated to {follow_up_status}. "
            f"Date: {follow_up_date}. Notes: {outcome_notes}",
            performed_by="Healthcare Staff"
        )

    return updated > 0


create_database()







