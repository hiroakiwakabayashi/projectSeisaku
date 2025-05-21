# kao_kintai_app/gui/worker_status_view.py

import customtkinter as ctk
from tkinter import ttk
import sqlite3
from datetime import datetime
import os

DB_PATH = "work_db.sqlite3"
HOURLY_WAGE = 1000  # 仮に時給1000円とする

def run():
    app = ctk.CTk()
    app.title("労働者 勤怠状況一覧")
    app.geometry("750x500")

    label_title = ctk.CTkLabel(app, text="🧑‍💼 勤怠状況一覧（読み取り専用）", font=("Arial", 20))
    label_title.pack(pady=20)

    tree_frame = ctk.CTkFrame(app)
    tree_frame.pack(pady=10, fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, columns=("id", "name", "days", "total_min", "salary"), show="headings")
    tree.heading("id", text="労働者ID")
    tree.heading("name", text="名前")
    tree.heading("days", text="勤務日数")
    tree.heading("total_min", text="総勤務時間（分）")
    tree.heading("salary", text="給与概算（円）")

    tree.column("id", width=100, anchor="center")
    tree.column("name", width=150, anchor="w")
    tree.column("days", width=100, anchor="center")
    tree.column("total_min", width=150, anchor="center")
    tree.column("salary", width=150, anchor="center")

    tree.pack(fill="both", expand=True)

    if not os.path.exists(DB_PATH):
        print("⚠ 勤怠用DBが見つかりません")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM workers")
    workers = cursor.fetchall()

    for wid, name in workers:
        cursor.execute("""
            SELECT start_time, end_time FROM attendance
            WHERE worker_id = ? AND start_time IS NOT NULL AND end_time IS NOT NULL
        """, (wid,))
        records = cursor.fetchall()

        total_minutes = 0
        for start_str, end_str in records:
            try:
                start = datetime.strptime(start_str, "%H:%M")
                end = datetime.strptime(end_str, "%H:%M")
                minutes = (end - start).seconds // 60
                total_minutes += minutes
            except Exception:
                continue

        days = len(records)
        salary = int(total_minutes / 60 * HOURLY_WAGE)
        tree.insert("", "end", values=(wid, name, days, total_minutes, f"{salary:,}"))

    conn.close()
    app.mainloop()
