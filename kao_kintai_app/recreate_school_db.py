# recreate_school_db.py
import os
import sqlite3

DB_PATH = "kao_kintai_app/school_db.sqlite3"

def recreate_school_db(db_path):
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️ 既存の {db_path} を削除しました")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        student_id TEXT UNIQUE,
        student_class TEXT,
        gender TEXT,
        email TEXT,
        face_id TEXT,
        password TEXT,
        department TEXT
    )
    """)

    conn.commit()
    conn.close()
    print(f"✅ 新しい {db_path} を作成しました。")

if __name__ == "__main__":
    recreate_school_db(DB_PATH)
