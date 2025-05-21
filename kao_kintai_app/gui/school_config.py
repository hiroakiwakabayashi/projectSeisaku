# kao_kintai_app/gui/school_config.py

import customtkinter as ctk
import os
import json
import sys
import bcrypt
import subprocess


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import school_db_initializer

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/school_config.json")

def run():
    app = ctk.CTk()
    app.title("学校用 - 詳細設定")
    app.geometry("600x750")

    # --- 基本設定 ---
    label_school = ctk.CTkLabel(app, text="学校名 / 学科名", font=("Arial", 14))
    label_school.pack(pady=(10, 5))
    entry_school = ctk.CTkEntry(app, width=300)
    entry_school.insert(0, "情報学科")
    entry_school.pack()

    label_db = ctk.CTkLabel(app, text="DBファイル名", font=("Arial", 14))
    label_db.pack(pady=(10, 5))
    entry_db = ctk.CTkEntry(app, width=300)
    entry_db.insert(0, "school_db.sqlite3")
    entry_db.pack()

        # --- 管理者ログイン情報 ---
    label_admin_id = ctk.CTkLabel(app, text="管理者ID", font=("Arial", 14))
    label_admin_id.pack(pady=(20, 5))
    entry_admin_id = ctk.CTkEntry(app, width=200)
    entry_admin_id.insert(0, "admin01")
    entry_admin_id.pack()

    label_admin_pass = ctk.CTkLabel(app, text="管理者パスワード", font=("Arial", 14))
    label_admin_pass.pack(pady=(10, 5))
    entry_admin_pass = ctk.CTkEntry(app, width=200, show="*")
    entry_admin_pass.pack()


    label_max_period = ctk.CTkLabel(app, text="最大授業コマ数", font=("Arial", 14))
    label_max_period.pack(pady=(10, 5))
    entry_max_period = ctk.CTkEntry(app, width=100)
    entry_max_period.insert(0, "5")
    entry_max_period.pack()

    label_late = ctk.CTkLabel(app, text="遅刻 → 欠席の境界（分）", font=("Arial", 14))
    label_late.pack(pady=(10, 5))
    entry_late = ctk.CTkEntry(app, width=100)
    entry_late.insert(0, "15")
    entry_late.pack()


    # --- 授業時間入力欄（動的） ---
    frame_classes = ctk.CTkFrame(app)
    frame_classes.pack(pady=(20, 5))

    class_time_entries = {}

    def update_class_time_entries():
        for widget in frame_classes.winfo_children():
            widget.destroy()
        class_time_entries.clear()

        try:
            max_periods = int(entry_max_period.get())
        except ValueError:
            return

        for i in range(1, max_periods + 1):
            label = ctk.CTkLabel(frame_classes, text=f"{i}限目", width=50)
            entry_start = ctk.CTkEntry(frame_classes, width=100)
            entry_start.insert(0, "09:00")
            entry_end = ctk.CTkEntry(frame_classes, width=100)
            entry_end.insert(0, "09:45")

            label.grid(row=i, column=0, padx=5, pady=2)
            entry_start.grid(row=i, column=1, padx=5, pady=2)
            entry_end.grid(row=i, column=2, padx=5, pady=2)

            class_time_entries[str(i)] = (entry_start, entry_end)

    entry_max_period.bind("<FocusOut>", lambda e: update_class_time_entries())
    update_class_time_entries()

    # --- 保存処理 ---
    def save_config():
        try:
            max_periods = int(entry_max_period.get())
            late_minutes = int(entry_late.get())
        except ValueError:
            print("⛔ 数値入力に誤りがあります")
            return

        # 授業時間
        class_times = {}
        for period, (start_entry, end_entry) in class_time_entries.items():
            start = start_entry.get().strip()
            end = end_entry.get().strip()
            class_times[period] = [start, end]

        # 管理者情報
        admin_id = entry_admin_id.get()
        admin_pass = entry_admin_pass.get()
        if not admin_id or not admin_pass:
            print("⚠ 管理者IDまたはパスワードが未入力です")
            return
        hashed_pass = bcrypt.hashpw(admin_pass.encode(), bcrypt.gensalt()).decode()

        # 設定をまとめて保存
        config = {
            "school_name": entry_school.get(),
            "db_path": entry_db.get(),
            "max_periods": max_periods,
            "late_threshold_minutes": late_minutes,
            "class_times": class_times,
            "admin_id": admin_id,
            "admin_password_hash": hashed_pass
        }

        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

        print("✅ 設定を保存:", config)
        school_db_initializer.init_school_db(config["db_path"])
        app.destroy()

        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "face_recognition_screen.py"))
        subprocess.Popen([sys.executable, script_path, "学校用"])



    save_btn = ctk.CTkButton(app, text="保存して完了", command=save_config)
    save_btn.pack(pady=30)

    app.mainloop()


