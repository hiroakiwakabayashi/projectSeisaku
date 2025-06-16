import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.db_utils import load_db_path

def run():
    app = ctk.CTk()
    app.title("勤怠履歴ビューア")
    app.geometry("700x500")

    label = ctk.CTkLabel(app, text="📋 勤怠履歴一覧", font=("Arial", 18))
    label.pack(pady=10)

    frame = ctk.CTkFrame(app)
    frame.pack(pady=10, fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("user_id", "action", "timestamp"), show="headings")
    tree.heading("user_id", text="社員番号")
    tree.heading("action", text="アクション")
    tree.heading("timestamp", text="日時")
    tree.column("user_id", width=100)
    tree.column("action", width=100)
    tree.column("timestamp", width=200)
    tree.pack(fill="both", expand=True)

    # スクロールバー
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # データベースから読み込み
    def load_data():
        db_path = load_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, action, timestamp FROM attendance ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)
        conn.close()

    load_data()

    ctk.CTkButton(app, text="閉じる", command=app.destroy).pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    run()
