import sqlite3
import os

DB_PATH = "school_db.sqlite3"  # 必要に応じて変更可

if not os.path.exists(DB_PATH):
    print(f"❌ データベースが存在しません: {DB_PATH}")
else:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute("DROP TABLE IF EXISTS students")
        conn.commit()
        print("✅ students テーブルを削除しました。")
    except Exception as e:
        print("❌ 削除に失敗:", e)
    finally:
        conn.close()
