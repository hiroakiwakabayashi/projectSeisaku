import customtkinter as ctk
import sqlite3
import os
import sys
import json

# 設定ファイルの読み込み
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/work_config.json"))

def load_db_path():
    if not os.path.exists(CONFIG_PATH):
        return "work_db.sqlite3"
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("db_path", "work_db.sqlite3")

def register_employee():
    emp_id = entry_id.get().strip()
    name = entry_name.get().strip()
    gender = gender_var.get()
    position = position_var.get()
    email = entry_email.get().strip()

    if not all([emp_id, name, gender, position, email]):
        result_label.configure(text="⚠️ 全ての項目を入力してください")
        return

    try:
        db_path = load_db_path()
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO employees (employee_id, name, gender, position, email)
            VALUES (?, ?, ?, ?, ?)
        """, (emp_id, name, gender, position, email))
        conn.commit()
        conn.close()
        result_label.configure(text="✅ 登録に成功しました", text_color="green")

        # 入力クリア
        entry_id.delete(0, ctk.END)
        entry_name.delete(0, ctk.END)
        entry_email.delete(0, ctk.END)
        gender_var.set("男性")
        position_var.set("社員")

    except Exception as e:
        result_label.configure(text=f"❌ DB登録エラー: {e}", text_color="red")

# GUI構築
app = ctk.CTk()
app.title("従業員登録")
app.geometry("400x480")

ctk.CTkLabel(app, text="従業員登録", font=("Arial", 20)).pack(pady=10)

entry_id = ctk.CTkEntry(app, placeholder_text="社員番号")
entry_id.pack(pady=5)

entry_name = ctk.CTkEntry(app, placeholder_text="名前")
entry_name.pack(pady=5)

gender_var = ctk.StringVar(value="男性")
ctk.CTkLabel(app, text="性別").pack()
gender_menu = ctk.CTkOptionMenu(app, values=["男性", "女性", "その他"], variable=gender_var)
gender_menu.pack(pady=5)

position_var = ctk.StringVar(value="社員")
ctk.CTkLabel(app, text="ポジション").pack()
position_menu = ctk.CTkOptionMenu(app, values=["社員", "アルバイト"], variable=position_var)
position_menu.pack(pady=5)

entry_email = ctk.CTkEntry(app, placeholder_text="メールアドレス")
entry_email.pack(pady=5)

ctk.CTkButton(app, text="登録", command=register_employee).pack(pady=15)

result_label = ctk.CTkLabel(app, text="", text_color="red")
result_label.pack()

ctk.CTkButton(app, text="終了", fg_color="gray", command=app.destroy).pack(pady=10)

app.mainloop()
