import customtkinter as ctk
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.db_utils import load_db_path

def run():
    app = ctk.CTk()
    app.title("従業員登録")
    app.geometry("400x400")

    ctk.CTkLabel(app, text="📋 従業員情報を入力してください", font=("Arial", 16)).pack(pady=10)

    entry_id = ctk.CTkEntry(app, placeholder_text="社員番号")
    entry_id.pack(pady=5)

    entry_name = ctk.CTkEntry(app, placeholder_text="名前")
    entry_name.pack(pady=5)

    entry_gender = ctk.CTkEntry(app, placeholder_text="性別")
    entry_gender.pack(pady=5)

    entry_email = ctk.CTkEntry(app, placeholder_text="メールアドレス")
    entry_email.pack(pady=5)

    result_label = ctk.CTkLabel(app, text="")
    result_label.pack(pady=10)

    def register():
        emp_id = entry_id.get().strip()
        name = entry_name.get().strip()
        gender = entry_gender.get().strip()
        email = entry_email.get().strip()

        if not emp_id or not name:
            result_label.configure(text="⚠ 社員番号と名前は必須です")
            return

        try:
            db_path = load_db_path()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO employees (id, name, gender, email)
                VALUES (?, ?, ?, ?)
            """, (emp_id, name, gender, email))
            conn.commit()
            result_label.configure(text="✅ 登録が完了しました")
            entry_id.delete(0, ctk.END)
            entry_name.delete(0, ctk.END)
            entry_gender.delete(0, ctk.END)
            entry_email.delete(0, ctk.END)
        except sqlite3.IntegrityError:
            result_label.configure(text="⚠ 既に登録されています")
        except Exception as e:
            result_label.configure(text=f"❌ エラー: {e}")
        finally:
            conn.close()

    ctk.CTkButton(app, text="登録", command=register).pack(pady=10)
    ctk.CTkButton(app, text="閉じる", command=app.destroy).pack(pady=5)

    app.mainloop()

if __name__ == "__main__":
    run()
