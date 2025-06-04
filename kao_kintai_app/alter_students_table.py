# alter_students_table.py
import sqlite3
import os

DB_PATH = "kao_kintai_app/school_db.sqlite3"

def alter_students_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(students);")
    existing_columns = [row[1] for row in cursor.fetchall()]

    new_columns = {
        "student_class": "TEXT",
        "gender": "TEXT",
        "email": "TEXT",
        "registered_at": "TEXT"
    }

    for col, col_type in new_columns.items():
        if col not in existing_columns:
            print(f"🔧 カラム追加中: {col}")
            cursor.execute(f"ALTER TABLE students ADD COLUMN {col} {col_type};")
        else:
            print(f"✅ カラム {col} は既に存在します")

    conn.commit()
    conn.close()
    print("✅ students テーブルの更新が完了しました。")

if __name__ == "__main__":
    if os.path.exists(DB_PATH):
        alter_students_table(DB_PATH)
    else:
        print(f"❌ データベースファイル {DB_PATH} が見つかりません。")
