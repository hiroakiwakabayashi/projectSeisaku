import sqlite3
import os

DB_PATH = "work_db.sqlite3"
SCHEMA_FILE = "work_schema.sql"

def init_work_db():
    if not os.path.exists(SCHEMA_FILE):
        print("❌ スキーマファイルが見つかりません")
        return

    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema = f.read()

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print("✅ 勤怠用データベースを初期化しました")

if __name__ == "__main__":
    init_work_db()
