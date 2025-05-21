# kao_kintai_app/gui/work_config.py

import customtkinter as ctk
import os
import json
import sys
import bcrypt
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import work_db_initializer


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/work_config.json")

def run():
    app = ctk.CTk()
    app.title("勤怠モード - 詳細設定")
    app.geometry("500x600")

    # 店舗名
    label_store = ctk.CTkLabel(app, text="店舗・事業所名", font=("Arial", 14))
    label_store.pack(pady=(20, 5))
    entry_store = ctk.CTkEntry(app, width=300)
    entry_store.pack()

    # DBファイル名
    label_db = ctk.CTkLabel(app, text="データベースファイル名", font=("Arial", 14))
    label_db.pack(pady=(20, 5))
    entry_db = ctk.CTkEntry(app, width=300)
    entry_db.insert(0, "work_db.sqlite3")
    entry_db.pack()

    # 勤務時間単位
    label_unit = ctk.CTkLabel(app, text="勤務時間の単位", font=("Arial", 14))
    label_unit.pack(pady=(20, 5))
    time_unit_var = ctk.StringVar(value="分単位")
    unit_option = ctk.CTkOptionMenu(app, values=["分単位", "時:分形式"], variable=time_unit_var)
    unit_option.pack()

    # 管理者ID・パスワード
    label_admin_id = ctk.CTkLabel(app, text="管理者ID", font=("Arial", 14))
    label_admin_id.pack(pady=(20, 5))
    entry_admin_id = ctk.CTkEntry(app, width=200)
    entry_admin_id.insert(0, "manager01")
    entry_admin_id.pack()

    label_admin_pass = ctk.CTkLabel(app, text="管理者パスワード", font=("Arial", 14))
    label_admin_pass.pack(pady=(10, 5))
    entry_admin_pass = ctk.CTkEntry(app, width=200, show="*")
    entry_admin_pass.pack()

    # 保存ボタン
    def save_config():
        store_name = entry_store.get()
        db_path = entry_db.get()
        time_unit = time_unit_var.get()

        admin_id = entry_admin_id.get()
        admin_pass = entry_admin_pass.get()

        if not admin_id or not admin_pass:
            print("⚠ 管理者ID または パスワードが未入力です")
            return

        hashed_pass = bcrypt.hashpw(admin_pass.encode(), bcrypt.gensalt()).decode()

        config = {
            "store_name": store_name,
            "db_path": db_path,
            "time_unit": time_unit,
            "admin_id": admin_id,
            "admin_password_hash": hashed_pass
        }

        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

        print("✅ 勤務モード設定を保存 & DB初期化")
        work_db_initializer.init_work_db(db_path)
        app.destroy()


        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "face_recognition_screen.py"))
        subprocess.Popen([sys.executable, script_path, "勤怠用"])



    save_btn = ctk.CTkButton(app, text="保存して完了", command=save_config)
    save_btn.pack(pady=40)

    app.mainloop()
