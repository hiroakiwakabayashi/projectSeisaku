# kao_kintai_app/db/school_db_initializer.py
import sqlite3
import os

def init_school_db(db_path: str):
    if os.path.exists(db_path):
        print(f"📂 既に {db_path} が存在しています。上書きはしません。")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 学生テーブル
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        student_id TEXT UNIQUE,
        face_id TEXT,
        password TEXT,
        department TEXT
    )
    """)

    # 出席記録テーブル
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        period INTEGER,
        status TEXT,
        remark TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """)

    # 時間割
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS class_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_of_week TEXT,
        period INTEGER,
        subject_name TEXT,
        professor_name TEXT
    )
    """)

    # 公欠・欠席理由
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS absences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        reason TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """)

    conn.commit()
    conn.close()
    print(f"✅ データベース {db_path} を作成・初期化しました。")
