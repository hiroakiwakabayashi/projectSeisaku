import customtkinter as ctk
import sqlite3
import pandas as pd

DB_PATH = "work_db.sqlite3"  # 勤怠用のDBパスに合わせてください

def run():
    app = ctk.CTk()
    app.title("勤怠確認")
    app.geometry("800x500")

    label = ctk.CTkLabel(app, text="📋 勤怠記録一覧", font=("Arial", 20))
    label.pack(pady=10)

    tree_frame = ctk.CTkFrame(app)
    tree_frame.pack(expand=True, fill="both", padx=20, pady=10)

    # Treeview風に表示（スクロール可能に）
    from tkinter import ttk
    tree = ttk.Treeview(tree_frame, columns=("date", "name", "action", "time", "position"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(side="left", fill="both", expand=True)

    # スクロールバー
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # データベースから勤怠データ取得
    def load_data():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT date, name, action, time, position FROM attendance")
        records = cursor.fetchall()
        conn.close()

        for row in records:
            tree.insert("", "end", values=row)

    load_data()

    ctk.CTkButton(app, text="閉じる", command=app.destroy).pack(pady=10)
    app.mainloop()

if __name__ == "__main__":
    run()
