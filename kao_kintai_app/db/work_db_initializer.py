# kao_kintai_app/db/work_db_initializer.py
import sqlite3
import os

def init_work_db(db_path: str):
    if os.path.exists(db_path):
        print(f"📂 既にDBファイル {db_path} が存在しています。上書きはしません。")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 労働者情報テーブル
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        face_id TEXT,
        role TEXT,
        password TEXT
    )
    """)

    # 勤務記録テーブル
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER,
        date TEXT,
        start_time TEXT,
        end_time TEXT,
        break_start TEXT,
        break_end TEXT,
        FOREIGN KEY(worker_id) REFERENCES workers(id)
    )
    """)

    # シフト予定
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shift_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER,
        shift_date TEXT,
        shift_start TEXT,
        shift_end TEXT,
        FOREIGN KEY(worker_id) REFERENCES workers(id)
    )
    """)

    conn.commit()
    conn.close()
    print(f"✅ データベース {db_path} を作成・初期化しました。")
