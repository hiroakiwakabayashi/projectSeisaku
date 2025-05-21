# kao_kintai_app/gui/student_status_view.py

import customtkinter as ctk
import sqlite3
import os
from tkinter import ttk
from tkinter import Scrollbar

DB_PATH = "school_db.sqlite3"

def run():
    app = ctk.CTk()
    app.title("学生 出席状況一覧")
    app.geometry("700x500")

    # タイトル
    label_title = ctk.CTkLabel(app, text="📋 出席状況一覧（読み取り専用）", font=("Arial", 20))
    label_title.pack(pady=20)

    # Treeview 表示部
    tree_frame = ctk.CTkFrame(app)
    tree_frame.pack(pady=10, fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, columns=("id", "name", "present", "total", "rate"), show="headings")
    tree.heading("id", text="学籍番号")
    tree.heading("name", text="名前")
    tree.heading("present", text="出席数")
    tree.heading("total", text="全コマ数")
    tree.heading("rate", text="出席率")

    tree.column("id", width=100, anchor="center")
    tree.column("name", width=150, anchor="w")
    tree.column("present", width=80, anchor="center")
    tree.column("total", width=80, anchor="center")
    tree.column("rate", width=100, anchor="center")

    tree.pack(fill="both", expand=True)

    # スクロールバー
    scrollbar = Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # データ読み込み
    if not os.path.exists(DB_PATH):
        print("⚠ school_db.sqlite3 が見つかりません")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT student_id, name FROM students")
    students = cursor.fetchall()

    for sid, name in students:
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id = ? AND status = '出席'", (sid,))
        present_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id = ?", (sid,))
        total_count = cursor.fetchone()[0]

        rate = f"{(present_count / total_count * 100):.1f}%" if total_count > 0 else "0.0%"
        tree.insert("", "end", values=(sid, name, present_count, total_count, rate))

    conn.close()

    app.mainloop()
