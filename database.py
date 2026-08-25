import sqlite3


DATABASE = "scam_reports.db"


# ==============================
# CREATE TABLE
# ==============================

def create_table():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scam_reports (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            message TEXT NOT NULL,

            category TEXT,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP

        )
    """)


    conn.commit()

    conn.close()


# ==============================
# SAVE REPORT
# ==============================

def save_report(message, category):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO scam_reports
        (message, category)

        VALUES (?, ?)
    """, (message, category))


    conn.commit()

    conn.close()